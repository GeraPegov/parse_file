from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.templating import Jinja2Templates

from app.application.services.parse_service import TourismService
from app.presentation.dependencies.get_tourism_service import get_tourism_service

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
    tourism_service: TourismService = Depends(get_tourism_service)
):
    contents = await file.read()
    result = await tourism_service.parse_file(contents)

    return result
    