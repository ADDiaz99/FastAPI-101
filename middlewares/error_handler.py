from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

#El error handler se encarga de manejar todos los errores de nuestra aplicacion, se implemente de la siguiente manera:
class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            return await call_next(request) #Al ser una funcion async, usamos el await
        except Exception as e:
            return JSONResponse(status_code=500, content={'error': str(e)}) 
        