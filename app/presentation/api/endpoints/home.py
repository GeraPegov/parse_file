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
    # data = await analysis_service.count_tourist_with_all_time()
    # data = await analysis_service.count_tourist_with_every_month()
    # data = await analysis_service.count_tourists_for_random_period()
    # data = await analysis_service.count_from_country()
    # data = await analysis_service.count_from_region()
    # data = await analysis_service.demographic_presentation()
    data = await analysis_service.average_tourists()
    return data
    