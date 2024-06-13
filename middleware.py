import asyncio
from fastapi import Request 
from logger import logger
from datetime import datetime 
import time 

async def middleware_log(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    log_dict ={
        'url': request.url.path,
        'method': request.method,
        'date': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'duration': duration
    }
    logger.info(log_dict,extra = log_dict)
    return response;