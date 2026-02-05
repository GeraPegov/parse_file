from fastapi import APIRouter, Request, UploadFile
from fastapi.templating import Jinja2Templates


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
    file: UploadFile = File(...)
)