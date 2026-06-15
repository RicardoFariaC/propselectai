from fastapi import APIRouter, HTTPException
from models.schemas import PropellerRequest, PropellerResponse, RecommendationResponse
from services.filters import get_recommendations
from services.rag import generate_justification
from services.report import generate_pdf_report

router = APIRouter()

@router.post("/recommend", response_model=RecommendationResponse)
def recommend_propellers(request: PropellerRequest):
    top_propellers = get_recommendations(request)
    
    if not top_propellers:
        raise HTTPException(status_code=404, detail="Nenhuma hélice atende aos requisitos ou o banco não retornou dados.")
        
    responses = []
    all_references = set()
    for prop in top_propellers:
        justification, refs = generate_justification(prop, request.mission_type)
        all_references.update(refs)
        responses.append(PropellerResponse(
            name=prop.get('nome_helice', 'Unknown'),
            diameter=float(prop.get('diametro', 0.0) or 0.0),
            pitch=float(prop.get('pitch', 0.0) or 0.0),
            efficiency=float(prop.get('eficiência', 0.0) or 0.0),
            thrust=float(prop.get('trust_n', 0.0) or 0.0),
            justification=justification
        ))
        
    report_filename = generate_pdf_report(request, responses, list(all_references))
    
    return RecommendationResponse(
        recommendations=responses,
        report_path=f"/data/pdf_gerados/{report_filename}",
        references=list(all_references)
    )
