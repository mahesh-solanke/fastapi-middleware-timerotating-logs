from fastapi import FastAPI,Request,Response
from datetime import datetime
import os
import logging
from celery.contrib import rdb
app  = FastAPI()

todays_date = datetime.now().date()
LOG_DIR = 'logs'
logger = logging.getLogger('custom_logger')

if LOG_DIR not in os.listdir():
    os.mkdir(LOG_DIR)
else:
    if str(datetime.now().date()) in os.listdir(LOG_DIR):
        file_name = os.path.join(LOG_DIR,str(datetime.now().date()),'custom.log')
        file_handler = logging.FileHandler(filename=file_name)
        custom_logger = logging.getLogger('custom_logger')
        custom_logger.setLevel(logging.DEBUG)
        custom_logger.addHandler(file_handler)
    else:
        os.mkdir(os.path.join(LOG_DIR, str(datetime.now().date())))
        file_name = os.path.join(LOG_DIR,str(datetime.now().date()),'custom.log')
        file_handler = logging.FileHandler(filename=file_name)
        custom_logger = logging.getLogger('custom_logger')
        custom_logger.setLevel(logging.DEBUG)
        custom_logger.addHandler(file_handler)
    

@app.middleware("http")
async def custom_logging_handler(request: Request,call_next):
    print('befor reuqets')
    custom_logger.info(f'test_log {str(datetime.now())}')
    response = await call_next(request) 
    cur_date = str(datetime.now().date())
    if cur_date not in os.listdir(LOG_DIR):
        custom_logger.info(f'initializing new log file {str(datetime.now())}')
        os.mkdir(LOG_DIR+"/"+cur_date)
        curdir = LOG_DIR+"/"+cur_date
        # if logging.getLogger().hasHandlers():
        logger = logging.getLogger('custom_logger')
        handler = MyFileHandler(curdir,logger,logging.FileHandler)
        logger.removeHandler((logger.handlers)[-1])
        logger.addHandler(handler)
        custom_logger.info(f'new log file initialized {str(datetime.now())}')
        
    print('after request')  
    return response
    

@app.get('/')
async def test():
    return {"message": "test api"}


class MyFileHandler(object):

    def __init__(self, dir, logger, handlerFactory, **kw):
        kw['filename'] = os.path.join(dir, 'custom.log')
        # kw['formatter'] = 'simple'
        self._handler = handlerFactory(**kw)

    def __getattr__(self, n):
        if hasattr(self._handler, n):
            return getattr(self._handler, n)
        raise AttributeError


