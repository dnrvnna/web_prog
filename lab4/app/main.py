from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.database import engine
from app.models.database import Base

app = FastAPI(title='Лабораторная работа №4', version='1.0.0')

Base.metadata.create_all(bind=engine)
app.include_router(router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={'message': 'Произошла ошибка на сервере.'},
    )


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=404,
        content={'message': str(exc)},
    )
