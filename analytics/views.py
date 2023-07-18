from django.shortcuts import render,get_object_or_404
from neomodel import db
from rest_framework.decorators import api_view
from rest_framework.response import Response

from station.entities import CrimeEntity, CriminalEntity
from users.entities import StationEntity
from shapely.geometry import Polygon
from users.models import Station

@api_view(["GET"])
def get_criminal_locations(request, id_number):
    query = """
    
        MATCH (c:Criminal {id_num: $criminalId})-[:COMMITTED]->(st:Station)
        RETURN DISTINCT c, st

            
    """
    params = {"criminalId": id_number}
    results, _meta = db.cypher_query(query, params)
    response = []
    for node in results:
        criminal_entity = CriminalEntity.inflate(node[0])
        station_entity = StationEntity.inflate(node[1])
        res = {
            "criminal": criminal_entity.__dict__(),
            "station": station_entity.__dict__(),
        }
        response.append(res)

    return Response(response)


# Create your views here.
@api_view(["GET"])
def get_all_crime_arrests(request):
    query = """

    MATCH (c:Criminal)<-[:ARRESTED]-(station:Station)
    WITH station, COLLECT(c) AS criminals, COUNT(c) AS numCriminals
    RETURN station, numCriminals

    """

    results, _meta = db.cypher_query(query)
    response = []
    for node in results:
        # criminal_entity = CriminalEntity.inflate(node[0])
        station_entity = StationEntity.inflate(node[0])
        station_dict = station_entity.__dict__()
        station_dict["num_criminals"] = node[1]
        res = {
            "station": station_dict,
        }
        response.append(res)

    return Response(response)


@api_view(["POST"])
def get_crime_arrests_filtered_by_crime(request):
    # cypher query to get criminal arrest details in respect to crime, a list of crimes to filter with will be provided in request.data and station

    query = """

    MATCH (s:Station)-[:ARRESTED]->(c:Criminal)-[ar:COMMITTED]->(cr:Crime)
    WHERE cr.entity_id IN $crimes
    RETURN c, s
    """

    crimes = request.data["crimes"]
    params = {"crimes": crimes}
    results, _meta = db.cypher_query(query, params)
    print(results)
    response = []
    for node in results:
        criminal_entity = CriminalEntity.inflate(node[0])
        station_entity = StationEntity.inflate(node[1])
        res = {
            "criminal": criminal_entity.__dict__(),
            "station": station_entity.__dict__(),
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
    
    MATCH (c:Criminal {id_num: $criminalId})-[:ARRESTED]-(s:Station)
    RETURN s

    
    """
    params = {"criminalId": criminal_id}
    results, _meta = db.cypher_query(query, params)
    response = []
    for node in results:
        station_entity = StationEntity.inflate(node[0])
        
        response.append(station_entity.__dict__())

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


@api_view(["GET"])
def criminal_accomplice_network(request, criminal_id):
    query = """
    
        MATCH (c:Criminal {id_num: $criminalId})-[:ACCOMPLICE*1..2]-(accomplice:Criminal)
        OPTIONAL MATCH (c)-[:COMMITTED]->(cr:Crime)
        WITH collect(DISTINCT c) + collect(DISTINCT accomplice) AS criminals, collect(DISTINCT cr) AS crimes
        UNWIND criminals AS criminal
        OPTIONAL MATCH (criminal)-[:COMMITTED]->(crime:Crime)
        RETURN criminal, collect(DISTINCT crime) AS crimes


            
    """
    params = {"criminalId": criminal_id}
    results, _meta = db.cypher_query(query, params)
    response = []
    for node in results:
        criminal_entity = CriminalEntity.inflate(node[0])
        crimes = [CrimeEntity.inflate(crime).__dict__() for crime in node[1]]

        res = {
            "criminal": criminal_entity.__dict__(),
            "crimes": crimes,
        }
        response.append(res)

    return Response(response)

@api_view(["GET"])
def crime_station_total_trend(request,station):
    query = """

    MATCH (s:Station {entity_id: $entity_id})
    OPTIONAL MATCH (s)-[:ARRESTED]-(c:Criminal)-[commited:COMMITTED]->(crime:Crime)
    WITH crime, datetime(commited.datetime).year AS month, COUNT(*) AS crimeCount
    RETURN month, SUM(crimeCount) AS totalCrimeCount
    ORDER BY month
    """
    station = get_object_or_404(Station,id=station)

    params = {
        "entity_id": station.id,
    }

    results, _meta = db.cypher_query(query, params)
    response = []
    total_crime_city = 0
    # sample response = {crime_counts:[1,2,3,4],months:[1,2,3,4],"total_crime_count":10}
    for node in results:
        total_crime_city += node[1]
        response.append({"month":node[0],"total_crime_count":node[1]})
    print(response)
    return Response(response)

@api_view(["GET"])
def crime_station_individual_total(request,station):
    # get total crime count for each crime commited in a station
    query = """
    
        MATCH (s:Station {entity_id: $entity_id})
        OPTIONAL MATCH (s)-[:ARRESTED]-(c:Criminal)-[commit:COMMITTED]->(crime:Crime)
        WITH crime.name AS crimeName, COUNT(*) AS crimeCount
        RETURN crimeName, crimeCount

    """

    station = get_object_or_404(Station,id=station)

    params = {
        "entity_id": station.id,
    }
    results, _meta = db.cypher_query(query, params)
    response = []
    for node in results:
        crime_name = node[0]
        crime_count = node[1]
        response.append({"crime_name":crime_name,"crime_count":crime_count})

    return Response(response)


def day_of_week_to_string(day):
    if day == 1:
        return "Monday"
    elif day == 2:
        return "Tuesday"
    elif day == 3:
        return "Wednesday"
    elif day == 4:
        return "Thursday"
    elif day == 5:
        return "Friday"
    elif day == 6:
        return "Saturday"
    elif day == 7:
        return "Sunday"
    
def hour_of_day_to_string(hour):
    if hour == 0:
        return "12am"
    elif hour == 1:
        return "1am"
    elif hour == 2:
        return "2am"
    elif hour == 3:
        return "3am"
    elif hour == 4:
        return "4am"
    elif hour == 5:
        return "5am"
    elif hour == 6:
        return "6am"
    elif hour == 7:
        return "7am"
    elif hour == 8:
        return "8am"
    elif hour == 9:
        return "9am"
    elif hour == 10:
        return "10am"
    elif hour == 11:
        return "11am"
    elif hour == 12:
        return "12pm"
    elif hour == 13:
        return "1pm"
    elif hour == 14:
        return "2pm"
    elif hour == 15:
        return "3pm"
    elif hour == 16:
        return "4pm"
    elif hour == 17:
        return "5pm"
    elif hour == 18:
        return "6pm"
    elif hour == 19:
        return "7pm"
    elif hour == 20:
        return "8pm"
    elif hour == 21:
        return "9pm"
    elif hour == 22:
        return "10pm"
    elif hour == 23:
        return "11pm"

@api_view(["GET"])
def crime_day_of_week_trend(request,crime):
    # get total crime count for each crime in respect to day of week
    from station.models import Crime
    query = """

        MATCH (crime:Crime {entity_id: $entity_id})
        OPTIONAL MATCH (crime)<-[commit:COMMITTED]-(c:Criminal)
        WITH crime.name AS crimeName, datetime(commit.datetime).dayOfWeek AS dayOfWeek, COUNT(*) AS crimeCount
        RETURN crimeName, crimeCount, dayOfWeek

    """
    crime = get_object_or_404(Crime,id=crime)
    results, _meta = db.cypher_query(query, {"entity_id": crime.id})
    print(results)
    response = []
    for node in results:
        
        crime_name = node[0]
        crime_count = node[1]
        day_of_week = day_of_week_to_string(node[2])
        response.append({"crime_name":crime_name,"crime_count":crime_count,"day_of_week":day_of_week})
    
    return Response(response)

@api_view(["GET"])
def crime_hour_of_day_trend(request,crime):
    # get total crime count for each crime in respect to hour of day
    from station.models import Crime
    query = """
    
        MATCH (crime:Crime {entity_id: $entity_id})
        OPTIONAL MATCH (crime)<-[commit:COMMITTED]-(c:Criminal)
        WITH crime.name AS crimeName, datetime(commit.datetime).hour AS hour, COUNT(*) AS crimeCount
        RETURN crimeName, crimeCount, hour

    """
    crime = get_object_or_404(Crime,id=crime)
    results, _meta = db.cypher_query(query, {"entity_id": crime.id})

    response = []
    for node in results:

        crime_name = node[0]
        crime_count = node[1]
        hour = hour_of_day_to_string(node[2])
        response.append({"crime_name":crime_name,"crime_count":crime_count,"hour":hour})
    return Response(response)


@api_view(["GET"])
def crime_station_chart(request,station):
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")

    if start_date and end_date:
        query = """
    
        MATCH (s:Station {entity_id: $entity_id})
        OPTIONAL MATCH (s)-[:ARRESTED]-(c:Criminal)-[commit:COMMITTED]->(crime:Crime)
        WHERE datetime(commit.datetime) >= datetime($start_date) AND datetime(commit.datetime) <= datetime($end_date)
        WITH crime.name AS crimeName, datetime(commit.datetime).month AS month, COUNT(*) AS crimeCount
        WITH crimeName, COLLECT(crimeCount) AS crimeCounts, COLLECT(month) AS months
        RETURN crimeName, crimeCounts, months
        ORDER BY crimeCounts DESC

    """
    else:
        query = """
        
            MATCH (s:Station {entity_id: $entity_id})
            OPTIONAL MATCH (s)-[:ARRESTED]-(c:Criminal)-[commit:COMMITTED]->(crime:Crime)
            WITH crime.name AS crimeName, datetime(commit.datetime).month AS month, COUNT(*) AS crimeCount
            WITH crimeName, COLLECT(crimeCount) AS crimeCounts, COLLECT(month) AS months
            RETURN crimeName, crimeCounts, months
            ORDER BY crimeCounts DESC

        """


    station = get_object_or_404(Station,id=station)

    params = {
        "entity_id": station.id,
        "start_date": request.query_params.get("start_date"),
        "end_date": request.query_params.get("end_date"),
    }

    results, _meta = db.cypher_query(query, params)
    # the result is in this format: [{crimename:"",crimeCount:[1,3],months:[1,2]}] make it a suitable response in this format:[{crimename:"".crimeCount:[0,0,0,1,1,0,0,1]}]
    response = []
    for node in results:
        crime_name = node[0]
        crime_counts = node[1]
        months = node[2]
        crime_dict = {"crime_name": crime_name, "crime_counts": [0] * 12}
        for i in range(len(months)):
            crime_dict["crime_counts"][months[i] - 1] = crime_counts[i]
        response.append(crime_dict)

    return Response(response)
