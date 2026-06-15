from .database import get_filtered_propellers

def calculate_thrust_requirement(weight_kg, engine_power_hp, cruise_speed_ms, altitude_m):
    # Modelo físico simplificado para calculo de arrasto 
    power_watts = engine_power_hp * 745.7
    speed = cruise_speed_ms if cruise_speed_ms > 0 else 1.0
    estimated_thrust = (power_watts / speed) * 0.7 
    min_thrust = weight_kg * 9.81 * 0.1  # L/D = 10 approx
    
    return max(estimated_thrust, min_thrust)

def get_recommendations(req):
    req_thrust = calculate_thrust_requirement(req.weight_kg, req.engine_power_hp, req.cruise_speed_ms, req.altitude_m)
    propellers = get_filtered_propellers(thrust_req=req_thrust, min_efficiency=0.5, max_diameter=req.max_diameter_inches)
    
    return propellers[:5]
