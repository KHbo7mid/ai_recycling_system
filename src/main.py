from fastapi import FastAPI
from routes import (health,router_classify,batch_router,helper_router)

from helpers.Settings import get_settings

app=FastAPI(
    title=get_settings.APP_NAME,
    version=get_settings.APP_VERSION,
    description="Garbage Classification API using YOLO and FastAPI",
    
)

app.include_router(health)
app.include_router(router_classify)
app.include_router(batch_router)
app.include_router(helper_router)

