from .database import get_filtered_propellers

def calculate_thrust_requirement(weight_kg, engine_power_hp, cruise_speed_ms):
    # Modelo físico simplificado para calculo de arrasto 
    power_watts = engine_power_hp * 745.7
    speed = cruise_speed_ms if cruise_speed_ms > 0 else 1.0
    estimated_thrust = (power_watts / speed) * 0.7

    min_thrust = weight_kg * 9.81 * 1/17  # L/D = 10 approx

    if estimated_thrust > min_thrust: 
        # Gera bons dados e boa eficiencia
        pass

    if estimated_thrust < min_thrust:
        # Da ruim!
        pass

    return { "min": min_thrust, "power": power_watts, "estimated": estimated_thrust, "speed": speed }

def get_recommendations(req):
    req_thrust = calculate_thrust_requirement(req.weight_kg, req.engine_power_hp, req.cruise_speed_ms)
    propellers = get_filtered_propellers(thrust_req=req_thrust["min"], min_efficiency=req_thrust["estimated"]*req_thrust["speed"]/req_thrust["power"], max_diameter=req.max_diameter_inches)
    
    return propellers
