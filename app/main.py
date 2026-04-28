from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from fastapi.exceptions import HTTPException
import time
import os

from app.api import router as api_router
from app.core.database import Base, engine
from app.core.limiter import limiter
from app.core.config import settings
from app.utils.logger import logger

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件
dist_path = os.path.join(os.path.dirname(__file__), "..", "dist")
assets_path = os.path.join(dist_path, "assets")
if os.path.exists(assets_path):
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")


# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"--> {request.method} {request.url.path} | IP: {request.client.host}")
    response = await call_next(request)
    duration = (time.time() - start_time) * 1000
    logger.info(f"<-- {request.method} {request.url.path} | Status: {response.status_code} | Duration: {duration:.2f}ms")
    return response

# 异常处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )

# 异常处理器
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"code": 429, "message": "请求过于频繁", "data": None})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"code": 500, "message": "服务器内部错误", "data": None})


# 注册 API 路由
app.include_router(api_router)


# SPA 回退
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    dist_index = os.path.join(os.path.dirname(__file__), "..", "dist", "index.html")
    if os.path.exists(dist_index):
        return FileResponse(dist_index)
    return JSONResponse(status_code=404, content={"code": 404, "message": "页面不存在", "data": None})