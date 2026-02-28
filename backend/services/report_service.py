"""
PDF Report generation service.

Builds a professional Heart Disease Risk Assessment PDF using ReportLab.
Separated from the route handler so the report layout can evolve
independently of the API wiring.
"""

import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from config import FEATURE_LABELS, FEATURE_INTERPRETATIONS, RISK_COLORS


def _hex_to_rgb(hex_color: str):
    """Convert a hex colour string to an (r, g, b) tuple scaled 0‑1."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))


def generate_pdf(data) -> BytesIO:
    """
    Generate a PDF report from a ReportRequest and return
    a seeked-to-zero BytesIO buffer.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 40

    # ----- Header -----
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, y, "Heart Disease Risk Assessment Report")
    c.setFont("Helvetica", 10)
    c.drawString(
        40, y - 20,
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    )
    y -= 50

    # ----- Patient Input Summary -----
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Patient Input Summary")
    y -= 20
    c.setFont("Helvetica", 10)

    features = [
        ("Age", data.age),
        ("Sex", data.sex),
        ("Chest Pain Type", data.cp),
        ("Resting BP", data.trestbps),
        ("Cholesterol", data.chol),
        ("Fasting Blood Sugar", data.fbs),
        ("Resting ECG", data.restecg),
        ("Max Heart Rate", data.thalach),
        ("Exercise Angina", data.exang),
        ("ST Depression", data.oldpeak),
        ("ST Slope", data.slope),
        ("Major Vessels", data.ca),
        ("Thalassemia", data.thal),
    ]
    for label, value in features:
        c.drawString(60, y, f"{label}: {value}")
        y -= 15
    y -= 10

    # ----- Risk Result -----
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Risk Result")
    y -= 20
    c.setFont("Helvetica", 12)

    risk_color = RISK_COLORS.get(data.risk_level, "#000")
    c.setFillColorRGB(*_hex_to_rgb(risk_color))
    c.drawString(60, y, f"Risk Level: {data.risk_level}")
    c.setFillColorRGB(0, 0, 0)
    c.drawString(200, y, f"Probability: {round(data.risk_probability * 100, 2)}%")
    y -= 20

    # ----- Top 5 Risk Factors -----
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Top 5 Risk Factors")
    y -= 20
    c.setFont("Helvetica", 10)

    for f in data.top_risk_factors[:5]:
        label = FEATURE_LABELS.get(f, f)
        interpretation = FEATURE_INTERPRETATIONS.get(f, "")
        shap_val = data.shap_values.get(f, 0)
        effect = "increasing" if shap_val >= 0 else "decreasing"
        color = (0.91, 0.29, 0.24) if effect == "increasing" else (0.15, 0.66, 0.38)
        c.setFillColorRGB(*color)
        c.drawString(60, y, f"{label}: {interpretation} ({effect} risk)")
        c.setFillColorRGB(0, 0, 0)
        y -= 15
    y -= 10

    # ----- Disclaimer -----
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Disclaimer")
    y -= 15
    c.setFont("Helvetica", 9)
    c.drawString(
        60, y,
        "This report is for educational purposes only and is not a substitute "
        "for professional medical advice.",
    )

    c.save()
    buffer.seek(0)
    return buffer
