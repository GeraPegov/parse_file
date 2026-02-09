from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.templating import Jinja2Templates

from app.application.services.analysis_service import AnalysisService
from app.application.services.parse_service import ParseService
from app.presentation.dependencies.get_analysis_service import get_analysis_service
from app.presentation.dependencies.get_parse_service import get_parse_service

router = APIRouter()

templates = Jinja2Templates('app/presentation/api/endpoints/templates')

@router.get('/')
async def home(
    request: Request
):
    return templates.TemplateResponse(
        'home.html',
        {'request': request}
    )

@router.post('/parse')
async def parse(
    file: UploadFile = File(...),
    tourism_service: ParseService = Depends(get_parse_service)
):
    contents = await file.read()
    result = await tourism_service.parse_file(contents)

    return result

@router.get('/analysis')
async def analysis(
    analysis_service: AnalysisService = Depends(get_analysis_service)
):
    data = await analysis_service.analysis_result()

    return 'ok'
    