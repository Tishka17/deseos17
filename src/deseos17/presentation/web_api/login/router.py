from fastapi import APIRouter, Request
from jinja2 import PackageLoader
from starlette.templating import Jinja2Templates

index_router = APIRouter()

jinja_loader = PackageLoader("deseos17.presentation.web_api.login")
templates = Jinja2Templates(directory="templates", loader=jinja_loader)


@index_router.get("/login")
def new_wish(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )
