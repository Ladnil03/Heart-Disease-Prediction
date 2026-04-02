"""
PDF Report generation service.

Builds a professional Heart Disease Risk Assessment PDF using ReportLab.
Separated from the route handler so the report layout can evolve
independently of the API wiring.
"""
# Fixes: FIX-4 (page-break logic), FIX-10 (long-text truncation)

import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from config import FEATURE_LABELS, FEATURE_INTERPRETATIONS, RISK_COLORS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hex_to_rgb(hex_color: str):
    """Convert a hex colour string to an (r, g, b) tuple scaled 0-1."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i: i + 2], 16) / 255 for i in (0, 2, 4))


def _safe_text(text: str, max_chars: int = 90) -> str:
    """Truncate text and append ellipsis if it exceeds max_chars. (FIX-10)"""
    text = str(text)
    return text if len(text) <= max_chars else text[: max_chars - 1] + "\u2026"


def _write_line(
    c,
    x: float,
    y: float,
    text: str,
    font: str = "Helvetica",
    size: int = 10,
    color: tuple = (0, 0, 0),
    page_height: float = 792,
    margin_bottom: float = 50,
) -> float:
    """
    Draw *text* at (x, y) on canvas *c*, automatically starting a new page
    when y would fall below *margin_bottom*. Returns the next y position.
    (FIX-4)
    """
    if y < margin_bottom:
        c.showPage()
        y = page_height - 40
        c.setFont(font, size)
    c.setFont(font, size)
    c.setFillColorRGB(*color)
    c.drawString(x, y, text)
    c.setFillColorRGB(0, 0, 0)
    return y - (size + 4)


# ---------------------------------------------------------------------------
# Main PDF generator
# ---------------------------------------------------------------------------

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
    y = _write_line(c, 40, y, "Heart Disease Risk Assessment Report",
                    font="Helvetica-Bold", size=18)
    y = _write_line(
        c, 40, y,
        _safe_text(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"),
        font="Helvetica", size=10,
    )
    y -= 20  # extra spacing after header

    # ----- Patient Input Summary -----
    y = _write_line(c, 40, y, "Patient Input Summary", font="Helvetica-Bold", size=14)
    y -= 6

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
        y = _write_line(c, 60, y, _safe_text(f"{label}: {value}"),
                        font="Helvetica", size=10)
    y -= 10

    # ----- Risk Result -----
    y = _write_line(c, 40, y, "Risk Result", font="Helvetica-Bold", size=14)
    y -= 6

    risk_color_hex = RISK_COLORS.get(data.risk_level, "#000000")
    risk_rgb = _hex_to_rgb(risk_color_hex)

    y = _write_line(c, 60, y, _safe_text(f"Risk Level: {data.risk_level}"),
                    font="Helvetica", size=12, color=risk_rgb)
    y = _write_line(
        c, 60, y,
        _safe_text(f"Probability: {round(data.risk_probability * 100, 2)}%"),
        font="Helvetica", size=12,
    )
    y -= 10

    # ----- Top 5 Risk Factors -----
    y = _write_line(c, 40, y, "Top 5 Risk Factors", font="Helvetica-Bold", size=14)
    y -= 6

    for f in data.top_risk_factors[:5]:
        label = FEATURE_LABELS.get(f, f)
        interpretation = FEATURE_INTERPRETATIONS.get(f, "")
        shap_val = data.shap_values.get(f, 0)
        effect = "increasing" if shap_val >= 0 else "decreasing"
        color = (0.91, 0.29, 0.24) if effect == "increasing" else (0.15, 0.66, 0.38)
        line_text = _safe_text(f"{label}: {interpretation} ({effect} risk)")
        y = _write_line(c, 60, y, line_text, font="Helvetica", size=10, color=color)
    y -= 10

    # ----- SHAP Values Detail -----
    y = _write_line(c, 40, y, "SHAP Feature Contributions", font="Helvetica-Bold", size=14)
    y -= 6

    for feat, sv in data.shap_values.items():
        feat_label = FEATURE_LABELS.get(feat, feat)
        sv_text = _safe_text(f"{feat_label}: {sv:+.4f}")
        y = _write_line(c, 60, y, sv_text, font="Helvetica", size=10)

    y -= 10
    base_text = _safe_text(f"Base value (expected value): {data.base_value:.4f}")
    y = _write_line(c, 60, y, base_text, font="Helvetica", size=10)
    y -= 16

    # ----- Disclaimer -----
    y = _write_line(c, 40, y, "Disclaimer", font="Helvetica-Bold", size=12)
    y = _write_line(
        c, 60, y,
        _safe_text(
            "This report is for educational purposes only and is not a substitute "
            "for professional medical advice."
        ),
        font="Helvetica", size=9,
    )

    c.save()
    buffer.seek(0)
    return buffer
