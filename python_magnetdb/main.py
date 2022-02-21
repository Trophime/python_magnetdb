from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from .config import static_files
from .routes.api.magnets import router as api_magnets_router
from .routes.api.materials import router as api_materials_router
from .routes.api.parts import router as api_parts_router
from .routes.api.sites import router as api_sites_router
from .routes.home import router as home_router
from .routes.magnets import router as magnets_router
from .routes.materials import router as materials_router
from .routes.parts import router as parts_router
from .routes.records import router as records_router
from .routes.sites import router as sites_router
from .routes.geom import router as geoms_router
from .routes.panels import router as panels_router
from .routes.simulations import router as simulations_router
from .routes.cfgs import router as cfgs_router
from .routes.model_jsons import router as jsons_router

app = FastAPI()

app.mount("/static", static_files, name="static")

app.include_router(home_router)
app.include_router(magnets_router)
app.include_router(materials_router)
app.include_router(sites_router)
app.include_router(parts_router)
app.include_router(records_router)
app.include_router(geoms_router)
app.include_router(simulations_router)
app.include_router(panels_router)
app.include_router(cfgs_router)
app.include_router(jsons_router)

app.include_router(api_materials_router)
app.include_router(api_parts_router)
app.include_router(api_magnets_router)
app.include_router(api_sites_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="MagnetDB API",
        version="2.5.0",
        description="OpenAPI schema for MagnetDB",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

