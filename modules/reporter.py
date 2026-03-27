from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from modules.utils import log

SEVERITY_COLORS = {
    "Critical": colors.HexColor("#dc2626"),
    "High":     colors.HexColor("#ea580c"),
    "Medium":   colors.HexColor("#d97706"),
    "Low":      colors.HexColor("#65a30d"),
    "Info":     colors.HexColor("#2563eb"),
}


def generate_report(domain: str, findings: list[dict]) -> str:
    path = f"output/{domain}/report.pdf"
    doc  = SimpleDocTemplate(path, leftMargin=2*cm, rightMargin=2*cm,
                             topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story  = []

    # Title
    story.append(Paragraph(f"CipherScan Security Report", styles["Title"]))
    story.append(Paragraph(f"Target: {domain}", styles["Heading2"]))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 0.5*cm))

    # Severity summary table
    counts = {}
    for f in findings:
        sev = f.get("severity", "Info")
        counts[sev] = counts.get(sev, 0) + 1

    summary_data = [["Severity", "Count"]]
    for sev in ["Critical", "High", "Medium", "Low", "Info"]:
        if sev in counts:
            summary_data.append([sev, str(counts[sev])])

    if len(summary_data) > 1:
        summary_table = Table(summary_data, colWidths=[8*cm, 4*cm])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND",  (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ("TEXTCOLOR",   (0, 0), (-1, 0), colors.white),
            ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.HexColor("#f8fafc"), colors.HexColor("#e2e8f0")]),
            ("GRID",        (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("ALIGN",       (1, 0), (1, -1), "CENTER"),
        ]))
        story.append(Paragraph("Summary", styles["Heading2"]))
        story.append(summary_table)
        story.append(Spacer(1, 0.5*cm))

    # Findings detail
    story.append(Paragraph("Findings", styles["Heading2"]))

    if not findings:
        story.append(Paragraph("No findings were identified.", styles["Normal"]))
    else:
        for i, f in enumerate(findings, 1):
            sev   = f.get("severity", "Info")
            color = SEVERITY_COLORS.get(sev, colors.gray)
            badge = ParagraphStyle(
                "badge", parent=styles["Normal"],
                textColor=color, fontName="Helvetica-Bold"
            )
            story.append(Paragraph(
                f"{i}. [{sev}] {f.get('type', 'Unknown')}", badge
            ))
            story.append(Paragraph(
                f.get("detail", "No detail available."), styles["Normal"]
            ))
            story.append(Spacer(1, 0.2*cm))

    doc.build(story)
    log(f"[✓] Report saved to {path}")
    return path
