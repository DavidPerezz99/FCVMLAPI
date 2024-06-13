from fastapi import FastAPI, status, Depends, HTTPException
from pydantic import BaseModel
import pandas as pd
from predict import predict
from predict import __version__ as model_version
import json
from logger import logger 
import asyncio
from middleware import middleware_log 
from starlette.middleware.base import BaseHTTPMiddleware 
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import auth
from auth import get_current_user


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

app.add_middleware(BaseHTTPMiddleware,dispatch = middleware_log)

logger.info('Starting FCV-MLAPI....')
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
async def user(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed.')
    return {'User':user}

@app.get("/home")
async def home():
    result = await asyncio.sleep(0)
    return {"health_check": "OK", "model_version": model_version}


@app.post("/predict", response_model=PredictionOut)
async def generate_inference(payload: BatchIn, user:user_dependency, db: db_dependency, status_code=status.HTTP_200_OK):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed.')
    else: 
        data = pd.DataFrame({"idAtencion":payload.idAtencion,
                             "nomSigno":payload.nomSigno,
                             "valor":payload.valor,
                             "fecRegistro":payload.fecRegistro}) 
        inferences = await predict(data)
        for item in inferences.columns:
            print(item)
        #print(json_inferences)
        np_inference = inferences.Inference.item()[0]
        inference = [float(x) for x in np_inference]
        print(type(inference))
        UserId = inferences.idAtencion.unique().item()
        UserId = int(UserId)
        #print(type(inferences))
        return {"idAtencion":UserId,
                "inferences":{'Arresto_Cardiaco':inference[0],
                              'Bajo_Gasto_Cardiaco':inference[1],
                              'Sano':inference[2],
                              'Shock_Cardiogenico':inference[3]},
                "State":inferences.State.unique().item()}
