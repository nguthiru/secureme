from django.shortcuts import render
from neomodel import db
from rest_framework.decorators import api_view
from rest_framework.response import Response

from station.entities import CrimeEntity, CriminalEntity
from users.entities import StationEntity
from shapely.geometry import Polygon


# Create your views here.
@api_view(["GET"])
def get_all_crime_arrests(request):
    query = """

    MATCH (c:Criminal)<-[:ARRESTED]-(station:Station)
    RETURN c, station

    """

    results, _meta = db.cypher_query(query)
    response = []
    for node in results:
        criminal_entity = CriminalEntity.inflate(node[0])
        station_entity = StationEntity.inflate(node[1])
        res = {
            "criminal": criminal_entity.__dict__(),
            "station_entity": station_entity.__dict__(),
        }
        response.append(res)

    return Response(response)


def create_bounding_box(polygon_coords):
    polygon = Polygon(polygon_coords)
    min_lng, min_lat, max_lng, max_lat = polygon.bounds
    return min_lng, min_lat, max_lng, max_lat


@api_view(["POST"])
def crimes_within_polygon(request):
    data = request.data
    points = data["polygon"]
    polygon_coords = [(point["lng"], point["lat"]) for point in points]

    min_lng, min_lat, max_lng, max_lat = create_bounding_box(polygon_coords)

    query = """

        MATCH (s:Station)-[:ARRESTED]->(c:Criminal)-[:COMMITTED]->(cr:Crime)
        WHERE s.longitude >= $minLng AND s.longitude <= $maxLng
        AND s.latitude >= $minLat AND s.latitude <= $maxLat
        RETURN DISTINCT c, cr, s

    """

    params = {
        "minLng": min_lng,
        "minLat": min_lat,
        "maxLng": max_lng,
        "maxLat": max_lat,
    }

    results, _meta = db.cypher_query(query, params)

    response = []
    for node in results:
        criminal_entity = CriminalEntity.inflate(node[0])
        crime_entity = CrimeEntity.inflate(node[1])
        station_entity = StationEntity.inflate(node[2])
        res = {
            "criminal": criminal_entity.__dict__(),
            "crime": crime_entity.__dict__(),
            "station": station_entity.__dict__(),
        }
        response.append(res)

    return Response(response)


@api_view(["GET"])
def get_criminal_arrest_locations(request, criminal_id):
    # return unique station locations where criminal was arrested

    query = """
    
    MATCH (cr:Crime)<-(c:Criminal {id_num: $criminalId})<-[:ARRESTED]-(station:Station)
    RETURN DISTINCT station,c,cr
    
    """
    params = {"criminalId": criminal_id}
    results, _meta = db.cypher_query(query, params)
    response = []
    for node in results:
        criminal_entity = CriminalEntity.inflate(node[1])
        station_entity = StationEntity.inflate(node[0])
        crime_entity = CrimeEntity.inflate(node[2])
        res = {
            "criminal": criminal_entity.__dict__(),
            "station": station_entity.__dict__(),
            "crime": crime_entity.__dict__(),
        }
        response.append(res)

    return Response(response)


@api_view(["GET"])
def get_criminal_arrests_details(request, criminal_id):
    # cypher query to get criminal arrest details in respect to crime, and station

    query = """

    MATCH (s:Station)-[:ARRESTED]->(c:Criminal {id_num:$criminalId})-[ar:COMMITTED]->(cr:Crime)
    RETURN s, c, cr,ar

    """
    params = {"criminalId": criminal_id}
    results, _meta = db.cypher_query(query, params)
    response = []
    for node in results:
        criminal_entity = CriminalEntity.inflate(node[1])
        station_entity = StationEntity.inflate(node[0])
        crime_entity = CrimeEntity.inflate(node[2])
        res = {
            "criminal": criminal_entity.__dict__(),
            "station": station_entity.__dict__(),
            "crime": crime_entity.__dict__(),
        }
        response.append(res)

    return Response(response)
