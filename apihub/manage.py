from fastapi import FastAPI
from routers import ollama_routers
from fastapi.openapi.models import Contact, License
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from database import engine
from models import Base

# Define custom OpenAPI info
custom_openapi_info = {
    "title": "APIHub",
    "default_version": "v1",
    "description": "API documentation for APIHUB",
    "terms_of_service": "https://www.example.com/terms/",
    "contact": {
        "email": "mohitnandaniya.contact@gmail.com"
    },
    "license": {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
}

# Create the FastAPI app with custom OpenAPI info
app = FastAPI(
    title=custom_openapi_info["title"],
    version=custom_openapi_info["default_version"],
    description=custom_openapi_info["description"],
    terms_of_service=custom_openapi_info["terms_of_service"],
    contact=Contact(email=custom_openapi_info["contact"]["email"]),
    license=License(name=custom_openapi_info["license"]["name"], url=custom_openapi_info["license"]["url"])
)

@app.get("/", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="apihub" + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title="apihub" + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )


@app.on_event("startup")
async def startup():
    # Ensure tables are created on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Include routers with the prefix 'api/v1/routers_name'
app.include_router(ollama_routers.router, prefix="/api/v1/ollama")