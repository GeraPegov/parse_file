from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.templating import Jinja2Templates

from app.application.services.parse_service import ParseService
from app.presentation.api.dependencies import get_parse_service


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
    parse_service: ParseService = Depends(get_parse_service())
):
    contents = await file.read()
    await parse_service.delete_dublicate(contents)
    