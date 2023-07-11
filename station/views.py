from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.models import Station
from users.serializers import StationSerializer
from neomodel import db
from rest_framework import status
from datetime import datetime
from .entities import CriminalEntity
from .serializers import CrimeSerializer
from .models import Crime
from rest_framework.viewsets import ModelViewSet
# Create your views here.
@api_view(["GET"])
def get_all_stations(request):
    stations = Station.objects.all()
    serializer = StationSerializer(stations, many=True)
    return Response(serializer.data)

class CrimeViewSet(ModelViewSet):
    serializer_class = CrimeSerializer
    queryset = Crime.objects.all()

@api_view(["GET"])
def check_if_criminal_exists(request, id_number):
    query = """

        MATCH (c:Criminal)
        WHERE c.id_num = $idNumber
        RETURN c

    """
    params = {"idNumber": id_number}
    results, meta = db.cypher_query(query, params,)
    if len(results) == 0:
        return Response(
            {"message": "Criminal not found"}, status=status.HTTP_404_NOT_FOUND
        )
    else:
        entity = CriminalEntity.inflate(results[0][0])

        return Response(entity.__dict__())

def create_arrest(station,criminal:CriminalEntity):
    query = """
        MATCH (s:Station),(c:Criminal)
        WHERE s.entity_id = $stationID AND c.id_num = $criminalID
        MERGE (s)-[a:ARRESTED]->(c)
        RETURN a
    """
    params = {
        "stationID": station.id,
        "criminalID": criminal.id_num
    }
    results, meta = db.cypher_query(query, params)
    return results

@api_view(["POST"])
def add_criminal(request):
    data = request.data
    id_num = data.get("idNumber")
    name = data.get("name")
    nickname = data.get("nickname")
    date_of_birth = data.get("dateOfBirth")
    image_url = data.get("imageUrl")
    height = data.get("height")

    #check if none is none
    if id_num is None or name is None or date_of_birth is None or image_url is None or height is None:
        return Response(
            {"error": "Please provide all the required fields"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    #convert date of birth to datetime object
    date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
    query = """
        MERGE (c:Criminal {id_num: $idNumber})
        ON CREATE SET c.name = $name, c.nickname = $nickname, c.date_of_birth = date($dateOfBirth), c.image_url = $imageUrl, c.height = $height
        RETURN c

    """
    params = {
        "idNumber": int(id_num),
        "name": name,
        "nickname": nickname,
        "dateOfBirth": date_of_birth.date().isoformat(),
        "imageUrl": image_url,
        "height": height,

    }

    results, meta = db.cypher_query(query, params)

    entity = CriminalEntity.inflate(results[0][0])
    station = request.user.station
    create_arrest(station,entity)
    return Response(entity.__dict__(), status=status.HTTP_201_CREATED)
    # except Exception as e:
    #     return Response(
    #         {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #     )

@api_view(['GET'])
def search_criminal(request):
    name = request.query_params.get('q')

    if  name is None:
        return Response(
            {"error": "Please provide either id or name"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    else:
        query="""
            MATCH (c:Criminal)
            WHERE c.name =~ '(?i).*' + $name + '.*'
            RETURN c

        """
        params = {
            "name": name
        }
        results, meta = db.cypher_query(query, params)
        if len(results) == 0:
            return Response(
                []
            )
        else:
            entities = [CriminalEntity.inflate(row[0]).__dict__() for row in results]
            return Response(entities)
@api_view(['POST'])  
def connect_crime(request):
    data = request.data

    #the crimes will come in as a list of dictionaries
    crime_id = data.get('crimeID')
    criminal_id = data.get('criminalID')
    datetime = data.get('time')
    casualities = data.get('casualities')
    #ensure all fields are provided
    if crime_id is None or criminal_id is None or datetime is None or casualities is None:
        return Response(
            {"error": "Please provide all the required fields"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    #connect crime and criminal with COMMITED relationship have the datetime and casualities as properties of the relationship
    query = """
        MATCH (c:Criminal),(cr:Crime) 
        WHERE c.id_num = $criminalID AND cr.entity_id = $crimeID
        MERGE (c)-[com:COMMITTED]->(cr)
        ON CREATE SET com.datetime = datetime($datetime), com.casualities = $casualities
        RETURN com
        """
    params = {
        "criminalID": int(criminal_id),
        "crimeID": int(crime_id),
        "datetime": datetime,
        "casualities": int(casualities)
    }
    results, meta = db.cypher_query(query, params)
    return Response(
        {'message': 'Crime connected to criminal successfully'}
    )

@api_view(['POST'])
def connect_accomplice(request):
    data = request.data
    criminalID = data.get('criminalID')
    accompliceID = data.get('accompliceID')
    if criminalID is None or accompliceID is None:
        return Response(
            {"error": "Please provide all the required fields"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    query = """
        MATCH (c1:Criminal),(c2:Criminal)
        WHERE c1.id_num = $criminalID AND c2.id_num = $accompliceID
        MERGE (c1)-[ac:ACCOMPLICE]->(c2)
        RETURN ac,c2,c1

    """
    params = {
        "criminalID": int(criminalID),
        "accompliceID": int(accompliceID)
    }
    results, meta = db.cypher_query(query, params)
    return Response(
        {'message': 'Accomplice connected to criminal successfully'},status=status.HTTP_201_CREATED
    )