import math

def haversine(center_latitude: float, center_longitude: float, point_latitude: float, point_longitude: float) -> float:
    '''
    Calculate the great circle distance between two points
    on the earth specified in decimal degrees
    :param center_latitude: Latitude of the first point (actual center)
    :param center_longitude: Longitude of the first point (actual center)
    :param point_latitude: Latitude of the second point
    :param point_longitude: Longitude of the second point
    :return: Air distance from the first to the second point
    '''
    # Convert decimal degrees to radians
    center_latitude, center_longitude, point_latitude, point_longitude = map(math.radians, [center_latitude, center_longitude, point_latitude, point_longitude])

    # Haversine formula
    d_longitude = point_longitude - center_longitude
    d_latitude = point_latitude - center_latitude
    a = math.sin(d_latitude / 2) ** 2 + math.cos(center_latitude) * math.cos(point_latitude) * math.sin(d_longitude / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c

    return distance


