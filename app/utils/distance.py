import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calcula a distância em metros entre dois pontos usando a fórmula de Haversine.
    """
    R = 6371000  # raio da Terra em metros
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def calculate_eta(bus_lat, bus_lon, dest_lat, dest_lon, speed_kmh):
    """
    Calcula o tempo estimado de chegada (ETA) em minutos.
    Se velocidade = 0, retorna None.
    """
    distance_m = haversine_distance(bus_lat, bus_lon, dest_lat, dest_lon)
    speed_mps = speed_kmh * 1000 / 3600  # converte km/h para m/s

    if speed_mps <= 0:
        return None  # ônibus parado ou velocidade inválida

    eta_seconds = distance_m / speed_mps
    eta_minutes = eta_seconds / 60

    return round(eta_minutes, 1)
