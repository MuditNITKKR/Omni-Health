from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_medical_pdf(filename="Sample_Biochemical_Report.pdf"):
    # Target file configuration
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Clinical Theme Styling
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1A365D"), # Deep Clinical Blue
        spaceAfter=15
    )
    
    section_heading = ParagraphStyle(
        'SectionH',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=15,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#2D3748")
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.white,
        alignment=1 # Centered
    )
    
    flag_high = ParagraphStyle('HighF', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#C53030"))
    flag_low = ParagraphStyle('LowF', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#2B6CB0"))
    flag_normal = ParagraphStyle('NormalF', parent=body_style, fontName='Helvetica', textColor=colors.HexColor("#2D3748"))

    story = []
    
    # 1. Header Banner
    story.append(Paragraph("METROPOLIS DIAGNOSTIC CLINICS", title_style))
    story.append(Paragraph("<b>Central Reference Laboratory Division</b> | ISO 15189 Certified", body_style))
    story.append(Spacer(1, 15))
    
    # 2. Patient Demographics Metadata Box
    demographics_data = [
        [Paragraph("<b>Patient Name:</b> John Doe", body_style), Paragraph("<b>Age / Gender:</b> 45 / Male", body_style)],
        [Paragraph("<b>Patient ID:</b> PT-2026-9940", body_style), Paragraph("<b>Date Collected:</b> 22-May-2026", body_style)],
        [Paragraph("<b>Referred By:</b> Dr. A. K. Sharma, MD", body_style), Paragraph("<b>Status:</b> Final Verified Report", body_style)]
    ]
    
    demo_table = Table(demographics_data, colWidths=[260, 260])
    demo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(demo_table)
    story.append(Spacer(1, 20))
    
    # 3. Comprehensive Panels
    story.append(Paragraph("Hematology & Glycemic Profile Assessments", section_heading))
    
    # Table data structures wrapping with paragraphs for dynamic auto-wrapping layout
    raw_panel_data = [
        ["Test Biomarker Suite", "Observed Result", "Physiological Reference Bounds", "Alert State"],
        ["Hemoglobin (Hb)", "11.2 g/dL", "13.8 - 17.2 g/dL", "LOW"],
        ["Total White Blood Cell Count", "14.2 K/µL", "4.5 - 11.0 K/µL", "HIGH"],
        ["Fasting Blood Glucose", "142 mg/dL", "70 - 100 mg/dL", "HIGH"],
        ["HbA1c (Glycated Hemoglobin)", "7.4 %", "4.0 - 5.6 %", "HIGH"],
        ["Serum Total Cholesterol", "265 mg/dL", "125 - 200 mg/dL", "HIGH"],
        ["High-Density Lipoprotein (HDL)", "32 mg/dL", "> 40 mg/dL", "LOW"],
        ["Low-Density Lipoprotein (LDL-C)", "185 mg/dL", "< 100 mg/dL", "HIGH"],
        ["Serum Creatinine", "0.9 mg/dL", "0.7 - 1.3 mg/dL", "NORMAL"]
    ]
    
    formatted_table_data = []
    # Header mapping
    formatted_table_data.append([Paragraph(cell, table_header_style) for cell in raw_panel_data[0]])
    
    # Rows mapping with clinical status coloring triggers
    for row in raw_panel_data[1:]:
        status = row[3]
        if status == "HIGH":
            status_p = Paragraph(status, flag_high)
        elif status == "LOW":
            status_p = Paragraph(status, flag_low)
        else:
            status_p = Paragraph(status, flag_normal)
            
        formatted_table_data.append([
            Paragraph(row[0], body_style),
            Paragraph(row[1], body_style),
            Paragraph(row[2], body_style),
            status_p
        ])
        
    panel_table = Table(formatted_table_data, colWidths=[180, 110, 140, 90])
    panel_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(panel_table)
    story.append(Spacer(1, 15))
    
    # 4. Clinical Impressions Section
    story.append(Paragraph("Clinical Interpretations & Diagnostic Notes", section_heading))
    findings_text = (
        "1. <b>Significant Leukocytosis:</b> Elevated WBC parameters imply systemic responses "
        "secondary to localized inflammatory markers or active infectious pathways.<br/>"
        "2. <b>Impaired Glycemic Regulation:</b> Uncontrolled HbA1c metrics (7.4%) match baseline "
        "criteria for active Type 2 Diabetes Mellitus pathologies.<br/>"
        "3. <b>Critical Atherogenic Risk Dyslipidemia:</b> Prominent elevation profiles of standard "
        "circulating LDL cholesterol particles flag strong associations with cardiovascular vulnerabilities."
    )
    story.append(Paragraph(findings_text, body_style))
    story.append(Spacer(1, 15))
    
    # 5. Electronic Authentication Footer block
    story.append(Paragraph("<b>Disclaimer:</b> This diagnostic assessment is an algorithmic generation configured for validation training metrics inside the Omni Health medical suite workflow frameworks.", body_style))
    
    doc.build(story)

if __name__ == "__main__":
    create_medical_pdf()
    print("Successfully generated 'Sample_Biochemical_Report.pdf'")