from fastapi import APIRouter, HTTPException
from models.schemas import PropellerRequest, PropellerResponse, RecommendationResponse
from services.filters import get_recommendations
from services.rag import generate_justification
from services.report import generate_pdf_report
import re

router = APIRouter()

@router.post("/recommend", response_model=RecommendationResponse)
def recommend_propellers(request: PropellerRequest):
    top_propellers = get_recommendations(request)
    
    if not top_propellers:
        raise HTTPException(status_code=404, detail="Nenhuma hélice atende aos requisitos ou o banco não retornou dados.")
        
    responses = []
    global_reference_map = {}
    
    for prop in top_propellers:
        justification_text, local_ref_map = generate_justification(prop, request)
        
        def replace_ref(match):
            local_idx = int(match.group(1))
            if local_idx in local_ref_map:
                ref_str = local_ref_map[local_idx]
                if ref_str not in global_reference_map:
                    global_reference_map[ref_str] = len(global_reference_map) + 1
                global_idx = global_reference_map[ref_str]
                return f"[{global_idx}]"
            return match.group(0)
            
        final_justification = re.sub(r'\[\s*(?:[Ff]onte\s*)?(\d+)\s*\]', replace_ref, justification_text)
        
        responses.append(PropellerResponse(
            name=prop.get('nome_helice', 'Unknown'),
            diameter=float(prop.get('diametro', 0.0) or 0.0),
            pitch=float(prop.get('pitch', 0.0) or 0.0),
            efficiency=float(prop.get('eficiência', 0.0) or 0.0),
            thrust=float(prop.get('trust_n', 0.0) or 0.0),
            justification=final_justification
        ))
        
    refs_list = [None] * len(global_reference_map)
    for ref_str, idx in global_reference_map.items():
        refs_list[idx-1] = f"[{idx}] {ref_str}"
        
    report_filename = generate_pdf_report(request, responses, refs_list)
    
    return RecommendationResponse(
        recommendations=responses,
        report_path=f"/data/pdf_gerados/{report_filename}",
        references=refs_list
    )
