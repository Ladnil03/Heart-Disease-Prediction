"""
Report route.

Generates and streams a PDF report for a completed prediction.
"""

from fastapi import APIRouter, Header
from fastapi.responses import StreamingResponse
from schemas import ReportRequest
from auth import verify_api_key
from services.report_service import generate_pdf

router = APIRouter(prefix="/api", tags=["Report"])


@router.post("/report")
def generate_report(data: ReportRequest, api_key: str = Header(..., alias="api-key")):
    verify_api_key(api_key)

    buffer = generate_pdf(data)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=Heart_Disease_Report.pdf"},
    )
