import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import uuid
import textwrap

def generate_pdf_report(request_data, recommendations, references):
    report_id = str(uuid.uuid4())[:8]
    filename = f"propselect_report_{report_id}.pdf"
    
    output_dir = "/app/data/pdf_gerados"
    if not os.path.exists(output_dir):
        output_dir = os.path.join(os.path.dirname(__file__), '../../../data/pdf_gerados')
        os.makedirs(output_dir, exist_ok=True)
        
    filepath = os.path.join(output_dir, filename)

    # ABNT: Margem esquerda 3cm (~85 pt), Margem direita 2cm (~56 pt)
    # A4 size: 595.27 x 841.89
    left_margin = 85
    
    c = canvas.Canvas(filepath, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(left_margin, 780, "PropSelectAI - Relatório de Decisão de Projeto")
    
    c.setFont("Helvetica", 12)
    c.drawString(left_margin, 750, f"Missão: {request_data.mission_type}")
    c.drawString(left_margin, 730, f"Peso: {request_data.weight_kg} kg | Potência: {request_data.engine_power_hp} HP")
    
    y = 690
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_margin, y, "Hélices Recomendadas:")
    y -= 30
    
    c.setFont("Helvetica", 11)
    for idx, rec in enumerate(recommendations):
        c.drawString(left_margin, y, f"{idx+1}. {rec.name}")
        c.drawString(left_margin + 20, y-15, f"Eficiência: {rec.efficiency:.2f} | Empuxo: {rec.thrust:.2f} N | Diâmetro: {rec.diameter}")
        
        lines = textwrap.wrap(f"Justificativa: {rec.justification}", width=80)
        y_just = y - 30
        for line in lines:
            c.drawString(left_margin + 20, y_just, line)
            y_just -= 15
            
        y = y_just - 20
        
        if y < 100:
            c.showPage()
            y = 780


    # Referências Bibliográficas
    y -= 20
    if y < 100:
        c.showPage()
        y = 780
        
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_margin, y, "Referências Bibliográficas (Padrão ABNT):")
    y -= 30
    
    c.setFont("Helvetica", 10)
    for ref in references:
        ref_lines = textwrap.wrap(ref, width=85)
        for line in ref_lines:
            if y < 50:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = 780
            c.drawString(left_margin, y, line)
            y -= 15
        y -= 10 

    c.save()
    return filename


