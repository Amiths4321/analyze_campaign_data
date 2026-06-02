import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_readable_pdf(json_data, output_pdf_path):
    # Setup document geometry
    doc = SimpleDocTemplate(
        output_pdf_path, 
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom Palette Styling
    primary_color = colors.HexColor("#1A365D")  # Dark Corporate Navy
    secondary_color = colors.HexColor("#2B6CB0") # Vibrant Accent Blue
    text_color = colors.HexColor("#2D3748")      # Charcoal Body Text
    
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], 
        fontName='Helvetica-Bold', fontSize=24, leading=28, 
        textColor=primary_color, spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'SectionHeader', parent=styles['Heading2'], 
        fontName='Helvetica-Bold', fontSize=14, leading=18, 
        textColor=secondary_color, spaceBefore=15, spaceAfter=8
    )
    
    body_style = ParagraphStyle(
        'BodyDark', parent=styles['Normal'], 
        fontName='Helvetica', fontSize=10, leading=14, 
        textColor=text_color, spaceAfter=6
    )
    
    table_text_style = ParagraphStyle(
        'TableText', parent=styles['Normal'], 
        fontName='Helvetica', fontSize=8, leading=10, textColor=text_color
    )
    
    table_header_style = ParagraphStyle(
        'TableHeaderText', parent=styles['Normal'], 
        fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white
    )

    # ---- 1. Document Title ----
    story.append(Paragraph("Marketing Campaign Analytics Report", title_style))
    story.append(Paragraph("Automated Strategic Performance Evaluation Dashboard", body_style))
    story.append(Spacer(1, 15))
    
    # ---- 2. AI Executive Summary Blocks ----
    ai = json_data.get("ai_insights", {})
    
    story.append(Paragraph("Executive Summary", h2_style))
    story.append(Paragraph(ai.get("executive_summary", "N/A"), body_style))
    
    story.append(Paragraph("Core Success Factors", h2_style))
    story.append(Paragraph(ai.get("success_factors", "N/A"), body_style))
    
    story.append(Paragraph("Immediate Corrective Actions", h2_style))
    story.append(Paragraph(ai.get("corrective_actions", "N/A"), body_style))
    
    story.append(Paragraph("Strategic Budget Reallocation", h2_style))
    story.append(Paragraph(ai.get("budget_reallocation", "N/A"), body_style))
    
    story.append(Spacer(1, 20))
    
    # ---- 3. Quantitative Performance Table ----
    story.append(Paragraph("Campaign Performance Metrics Breakdown", h2_style))
    
    # Define Table Structural Headers
    headers = ["Campaign Name", "Channel", "Spend ($)", "Revenue ($)", "CTR (%)", "CPC ($)", "Conv. (%)", "ROAS"]
    table_data = [[Paragraph(h, table_header_style) for h in headers]]
    
    # Append Rows from Data Matrix
    for c in json_data.get("performance_metrics", []):
        row = [
            Paragraph(c['campaign_name'], table_text_style),
            Paragraph(c['channel'], table_text_style),
            Paragraph(f"{c['spend']:,}", table_text_style),
            Paragraph(f"{c['revenue']:,}", table_text_style),
            Paragraph(str(c['CTR_percent']), table_text_style),
            Paragraph(str(c['CPC']), table_text_style),
            Paragraph(str(c['Conversion_Rate_percent']), table_text_style),
            Paragraph(str(c['ROAS']), table_text_style)
        ]
        table_data.append(row)
        
    # Column Width Matrix (adds up to 532 points available layout space)
    col_widths = [115, 65, 52, 55, 45, 45, 45, 40]
    
    metrics_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    
    # Format Table Visual Board borders and shading
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
    ]))
    
    story.append(metrics_table)
    
    # Build Document File
    doc.build(story)
    print(f"✅ Success! Readable executive PDF generated safely at: {output_pdf_path}")

if __name__ == "__main__":
    # Raw payload data directly matching your structured JSON response block
    raw_payload = {
        "performance_metrics": [
            {"campaign_id": "CMP_001", "campaign_name": "Summer Sale Meta", "channel": "Meta", "spend": 5000, "impressions": 250000, "clicks": 7500, "conversions": 180, "revenue": 9000, "CTR_percent": 3.0, "CPC": 0.67, "Conversion_Rate_percent": 2.4, "ROAS": 1.8},
            {"campaign_id": "CMP_002", "campaign_name": "Google Search Brand", "channel": "Google Search", "spend": 12000, "impressions": 450000, "clicks": 22000, "conversions": 850, "revenue": 42500, "CTR_percent": 4.89, "CPC": 0.55, "Conversion_Rate_percent": 3.86, "ROAS": 3.54},
            {"campaign_id": "CMP_003", "campaign_name": "LinkedIn B2B Outreach", "channel": "LinkedIn", "spend": 8500, "impressions": 80000, "clicks": 1200, "conversions": 32, "revenue": 4800, "CTR_percent": 1.5, "CPC": 7.08, "Conversion_Rate_percent": 2.67, "ROAS": 0.56},
            {"campaign_id": "CMP_004", "campaign_name": "Retargeting Display", "channel": "Display", "spend": 3100, "impressions": 190000, "clicks": 2100, "conversions": 45, "revenue": 2100, "CTR_percent": 1.11, "CPC": 1.48, "Conversion_Rate_percent": 2.14, "ROAS": 0.68},
            {"campaign_id": "CMP_005", "campaign_name": "Newsletter Blast Q2", "channel": "Email", "spend": 450, "impressions": 35000, "clicks": 1800, "conversions": 95, "revenue": 5700, "CTR_percent": 5.14, "CPC": 0.25, "Conversion_Rate_percent": 5.28, "ROAS": 12.67},
            {"campaign_id": "CMP_006", "campaign_name": "Influencer Pack Tech", "channel": "Influencer", "spend": 15000, "impressions": 600000, "clicks": 18000, "conversions": 210, "revenue": 16800, "CTR_percent": 3.0, "CPC": 0.83, "Conversion_Rate_percent": 1.17, "ROAS": 1.12},
            {"campaign_id": "CMP_007", "campaign_name": "Google Shopping Apparel", "channel": "Google Shopping", "spend": 9200, "impressions": 310000, "clicks": 14000, "conversions": 410, "revenue": 24600, "CTR_percent": 4.52, "CPC": 0.66, "Conversion_Rate_percent": 2.93, "ROAS": 2.67},
            {"campaign_id": "CMP_008", "campaign_name": "Meta Lookalike Audience", "channel": "Meta", "spend": 6000, "impressions": 280000, "clicks": 8900, "conversions": 290, "revenue": 17400, "CTR_percent": 3.18, "CPC": 0.67, "Conversion_Rate_percent": 3.26, "ROAS": 2.9},
            {"campaign_id": "CMP_009", "campaign_name": "YouTube Pre-Roll Tech", "channel": "YouTube", "spend": 11000, "impressions": 850000, "clicks": 9500, "conversions": 110, "revenue": 8800, "CTR_percent": 1.12, "CPC": 1.16, "Conversion_Rate_percent": 1.16, "ROAS": 0.8},
            {"campaign_id": "CMP_010", "campaign_name": "X Promo Devs", "channel": "X", "spend": 2500, "impressions": 120000, "clicks": 3100, "conversions": 65, "revenue": 3900, "CTR_percent": 2.58, "CPC": 0.81, "Conversion_Rate_percent": 2.1, "ROAS": 1.56}
        ],
        "ai_insights": {
            "executive_summary": "The campaign demonstrated a blended ROAS of 1.86, indicating a return on ad spend above the industry's benchmark. The Newsletter Blast Q2 campaign excelled significantly with a ROAS of 12.67 and a Conversion Rate of 5.28%. However, underperforming campaigns like LinkedIn B2B Outreach and Retargeting Display also highlight areas for improvement with ROAS of 0.56 and 0.68, respectively.",
            "success_factors": "The success should be attributed to the targeted campaign execution and the relevance of the emails with the target audience, leading to a higher conversion rate and ROAS.",
            "corrective_actions": "Implement performance optimization strategies for underperforming campaigns by adjusting targeting, frequency, and creative content to align more closely with customer interest and behavior.",
            "budget_reallocation": "Reallocate budget based on campaign performance, prioritizing re-investment into high-performing channels like email or Google Search. Also, further refine ad strategies and targeting to boost ROAS across all campaigns."
        }
    }
    
    # Save target report file into your folder setup
    os.makedirs("Work on", exist_ok=True)
    target_pdf = os.path.join("Work on", "Marketing_Campaign_Analysis.pdf")
    create_readable_pdf(raw_payload, target_pdf)