from fastapi import FastAPI, status, Depends, HTTPException  # type: ignore
from pydantic import BaseModel  # type: ignore
import requests
import asyncio
from starlette.middleware.base import BaseHTTPMiddleware  # type: ignore
from app.database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session  # type: ignore
from app.routes import auth
from app.routes.auth import get_current_user
from app.utils.logger import logger
from app.utils.middleware import middleware_log
from app.utils import models


app = FastAPI()
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

app.add_middleware(BaseHTTPMiddleware, dispatch=middleware_log)

logger.info("Starting FCV-MLAPI....")


class BatchIn(BaseModel):
    idAtencion: int
    idSigno: dict
    nomSigno: dict
    valor: dict
    fecRegistro: dict


class PredictionOut(BaseModel):
    idAtencion: int
    inferences: dict
    State: str


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    """
    Retrieve user information.

    Parameters:
    - user: The user object containing user information.
    - db: The database dependency.

    Returns:
    - A dictionary containing the user information.

    Raises:
    - HTTPException with status code 401 if authentication fails.
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    return {"User": user}


@app.get("/home")
async def home():
    """
    Endpoint for the home page.

    Returns:
        dict: A dict containing the health check status and model version.
    """
    await asyncio.sleep(0)  # type: ignore
    model_version = "1.0.0"
    return {"health_check": "OK", "model_version": model_version}


@app.post("/predict", response_model=PredictionOut)
async def generate_inference(
    payload: BatchIn,
    user: user_dependency,
    db: db_dependency,
    status_code=status.HTTP_200_OK,
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    else:
        data = {
            "idAtencion": payload.idAtencion,
            "nomSigno": payload.nomSigno,
            "valor": payload.valor,
            "fecRegistro": payload.fecRegistro,
            }

        # inferences = await predict(data)
        port_HTTP = '5000'
        # ip = "127.0.0.1"
        ip = "localhost"
        uri = ''.join(['http://', ip, ':', port_HTTP, '/models'])
        # print(data)

        # Include the JWT token in the request headers
        headers = {"token": user["token"]}
        # headers = {"token": "asdasd"}
        # print(headers)

        try:
            inferences = requests.post(uri, json=data, headers=headers)
            # Check if the response status code
            # indicates a client or server error
            if inferences.status_code >= 400:
                # Extract error detail from the response, if available
                error_detail = inferences.json().get(
                    'detail', 'Error connecting to model endpoint'
                )
                raise HTTPException(status_code=inferences.status_code,
                                    detail=error_detail)
        except requests.exceptions.RequestException as e:
            # Handle other request exceptions, such as connection errors
            raise HTTPException(status_code=503, detail=str(e))

        # Ensure the response is JSON serializable
        try:
            response_json = inferences.json()
        # except ValueError as e:
        except ValueError as e:
            return {"error": "Invalid JSON response from model endpoint",
                    "message": str(e)}

        return response_json
