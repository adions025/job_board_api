from fastapi import APIRouter
from apis.version1 import route_users
from apis.version1 import route_jobs
from apis.version1 import route_login

api_router = APIRouter()
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(route_login.router, prefix="/login", tags=["login"])


# @api_router.get("/openapi.json")
# async def get_open_api_endpoint(current_user: User = Depends(get_current_active_user)):
#     return JSONResponse(get_openapi(title="FastAPI", version=1, routes=app.routes))
#
#
# @api_router.get("/documentation")
# async def get_documentation(current_user: User = Depends(get_current_active_user)):
#     return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
