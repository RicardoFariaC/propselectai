import sys
import os

sys.path.append('/home/ricardo/Documents/Mestrado/Aulas/IA_2026_1/EXAME/backend')

from models.schemas import PropellerRequest
from services.rag import generate_justification

prop = {
    'nome_helice': 'APC 10x5E',
    'diametro': 10,
    'pitch': 5,
    'eficiência': 0.75,
    'trust_n': 15.0
}
req = PropellerRequest(
    mission_type='reconhecimento',
    weight_kg=2.5,
    engine_power_hp=1.0,
    cruise_speed_ms=10.0
)

try:
    text, refs = generate_justification(prop, req)
    print("TEXT:")
    print(text)
    print("REFS:")
    print(refs)
except Exception as e:
    print("Error:", e)
