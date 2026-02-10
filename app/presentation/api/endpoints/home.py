from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.application.services.analysis_service import AnalysisService
from app.application.services.management_database_service import (
    ManagementDatabaseService,
)
from app.application.services.parse_service import ParseService
from app.presentation.dependencies.get_management_service import get_management_service
from app.presentation.dependencies.get_analysis_service import get_analysis_service
from app.presentation.dependencies.get_parse_service import get_parse_service

router = APIRouter()

templates = Jinja2Templates("app/presentation/api/endpoints/templates")


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.post("/tourism-data")
async def upload_tourism_data(
    upload_file: UploadFile = File(...),
    parse_service: ParseService = Depends(get_parse_service),
):
    contents = await upload_file.read()
    result = await parse_service.parse_file(contents)
    return result


@router.get("/tourism-data/analysis")
async def tourism_analysis(
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    filepath = await analysis_service.generate_analysis_report()

    return FileResponse(
        path=filepath, filename="tourism_analysis.json", media_type="application/json"
    )


@router.post("/tourism-data/clear")
async def delete(
    management_service: ManagementDatabaseService = Depends(get_management_service),
):
    await management_service.drop_table()
    return RedirectResponse(url="/", status_code=303)
