from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from app.core.config import PAGE_METADATA
from app.tobaccos.dao import BrandDAO, FlavourDAO, CategoryDAO, TobaccoDAO
from app.tobaccos.router import router as api_router


# Cache for tobacco assortment page.
TOBACCO_FLAVOURS = []
TOBACCO_BRANDS = []
TOBACCO_CATEGORIES = []
TOBACCO_STRENGTH = []


@asynccontextmanager
async def lifespan(application: FastAPI):
    global TOBACCO_BRANDS, TOBACCO_CATEGORIES, TOBACCO_FLAVOURS,TOBACCO_STRENGTH
    TOBACCO_BRANDS = await BrandDAO.find_all()

    TOBACCO_BRANDS = [
        {"name": item.name, "id": item.id} for item in TOBACCO_BRANDS
    ]
    TOBACCO_BRANDS.sort(key=lambda item: item["name"])

    TOBACCO_CATEGORIES = await CategoryDAO.find_all()
    TOBACCO_CATEGORIES = [
        {"name": item.name, "id": item.id} for item in TOBACCO_CATEGORIES
    ]

    TOBACCO_FLAVOURS = await FlavourDAO.find_all()
    TOBACCO_FLAVOURS = [
        {"name": item.name, "id": item.id} for item in TOBACCO_FLAVOURS
    ]
    TOBACCO_FLAVOURS.sort(key=lambda item: item["name"])

    TOBACCO_STRENGTH = await TobaccoDAO.get_strength_list()

    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        name = "info.html",
        context = {
            "request": request,
            "title": PAGE_METADATA["title"],
            "copyright": PAGE_METADATA["copyright"],
            "gm_url": PAGE_METADATA["gm_url"],
            "inst_url": PAGE_METADATA["inst_url"],
            "tg_url": PAGE_METADATA["tg_url"],
        },
    )


@app.get("/tobacco")
async def tobacco_page(request: Request):
    tobacco = await TobaccoDAO.find_all()

    return templates.TemplateResponse(
        name = "tobacco.html",
        context = {
            "request": request,
            "title": PAGE_METADATA["title"],
            "copyright": PAGE_METADATA["copyright"],
            "gm_url": PAGE_METADATA["gm_url"],
            "inst_url": PAGE_METADATA["inst_url"],
            "tg_url": PAGE_METADATA["tg_url"],
            "flavours": TOBACCO_FLAVOURS,
            "brands": TOBACCO_BRANDS,
            "categories": TOBACCO_CATEGORIES,
            "strength": TOBACCO_STRENGTH,
            "tobacco": tobacco,
        },
    )


@app.get("/news")
async def news_page(request: Request):
    return templates.TemplateResponse(
        name = "news.html",
        context = {
            "request": request,
            "title": PAGE_METADATA["title"],
            "copyright": PAGE_METADATA["copyright"],
            "gm_url": PAGE_METADATA["gm_url"],
            "inst_url": PAGE_METADATA["inst_url"],
            "tg_url": PAGE_METADATA["tg_url"],
        },
    )


app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
