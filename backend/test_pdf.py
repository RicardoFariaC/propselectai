from models.schemas import PropellerRequest, PropellerResponse
from services.report import generate_pdf_report

req = PropellerRequest(
    mission_type='reconhecimento',
    weight_kg=2.5,
    engine_power_hp=1.0,
    cruise_speed_ms=10.0
)
resp = PropellerResponse(
    name='APC',
    diameter=10,
    pitch=5,
    efficiency=0.75,
    thrust=15.0,
    justification='Justification'
)

generate_pdf_report(req, [resp], ["[1] DOC1", "[2] DOC2"])
