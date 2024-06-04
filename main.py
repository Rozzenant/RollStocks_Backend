from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from scr.rolls.router import router as router_rolls
from fastapi.encoders import jsonable_encoder

app = FastAPI(
    title="RollStock Backend"
)


@app.exception_handler(HTTPException)
async def HTTPException_exception_handler(request: Request,
                                          exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(exc)
    )


@app.exception_handler(OSError)
async def OSError_exception_handler(request: Request, exc: OSError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "detail": str(exc)
            },
    )

app.include_router(router_rolls)
