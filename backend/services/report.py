import os
import uuid
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import cm

def generate_pdf_report(request_data, recommendations, references):
    report_id = str(uuid.uuid4())[:8]
    filename = f"propselect_report_{report_id}.pdf"
    
    output_dir = "/app/data/pdf_gerados"
    if not os.path.exists(output_dir):
        output_dir = os.path.join(os.path.dirname(__file__), '../../../data/pdf_gerados')
        os.makedirs(output_dir, exist_ok=True)
        
    filepath = os.path.join(output_dir, filename)

    # ABNT: Margem esquerda 3cm, Margem superior 3cm, Margem direita 2cm, Margem inferior 2cm
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=3*cm,
        topMargin=3*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles['Heading1'],
        fontName="Helvetica-Bold",
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    info_style = ParagraphStyle(
        "InfoStyle",
        parent=styles['Normal'],
        fontName="Helvetica",
        fontSize=12,
        spaceAfter=5
    )
    
    bold_style = ParagraphStyle(
        "BoldHeading",
        parent=styles['Normal'],
        fontName="Helvetica-Bold",
        fontSize=14,
        spaceBefore=20,
        spaceAfter=10
    )
    
    rec_title_style = ParagraphStyle(
        "RecTitle",
        parent=styles['Normal'],
        fontName="Helvetica-Bold",
        fontSize=12,
        spaceBefore=15,
        spaceAfter=5
    )
    
    rec_data_style = ParagraphStyle(
        "RecData",
        parent=styles['Normal'],
        fontName="Helvetica",
        fontSize=11,
        leftIndent=20,
        spaceAfter=5
    )
    
    justified_indent_style = ParagraphStyle(
        "JustifiedIndent",
        parent=styles['Normal'],
        fontName="Helvetica",
        fontSize=11,
        alignment=TA_JUSTIFY,
        leftIndent=20,
        spaceAfter=10
    )
    
    ref_style = ParagraphStyle(
        "RefStyle",
        parent=styles['Normal'],
        fontName="Helvetica",
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=10
    )

    story = []
    
    # Header
    story.append(Paragraph("PropSelectAI - Relatório de Decisão de Projeto", title_style))
    
    # Escaping any dynamic user/DB content is safer when using Paragraphs
    mission_safe = escape(str(request_data.mission_type))
    weight_safe = escape(str(request_data.weight_kg))
    power_safe = escape(f"{request_data.engine_power_hp}")
    
    story.append(Paragraph(f"<b>Missão:</b> {mission_safe}", info_style))
    story.append(Paragraph(f"<b>Peso:</b> {weight_safe} kg | <b>Potência:</b> {power_safe} HP | <b>Velocidade de Cruzeiro</b>: {request_data.cruise_speed_ms} m/s", info_style))
    story.append(Spacer(1, 10))
    
    # Recommendations
    story.append(Paragraph("Hélices Recomendadas:", bold_style))
    
    for idx, rec in enumerate(recommendations):
        rec_name_safe = escape(str(rec.name))
        story.append(Paragraph(f"{idx+1}. {rec_name_safe}", rec_title_style))
        
        data_text = f"Eficiência: {rec.efficiency:.2f} | Empuxo: {rec.thrust:.2f} N | Diâmetro: {escape(str(rec.diameter))}"
        story.append(Paragraph(data_text, rec_data_style))
        
        justification_text = f"<b>Justificativa:</b> {escape(rec.justification)}"
        story.append(Paragraph(justification_text, justified_indent_style))
        
    story.append(Spacer(1, 15))
    
    # References
    if references:
        story.append(Paragraph("Referências Bibliográficas (Padrão ABNT):", bold_style))
        for ref in references:
            story.append(Paragraph(escape(ref), ref_style))
    else:
        story.append(Paragraph("Referências Bibliográficas (Padrão ABNT):", bold_style))
        story.append(Paragraph("Nenhuma referência bibliográfica disponível para esta análise.", ref_style))

    # Generate the PDF Document
    doc.build(story)
    
    return filename



