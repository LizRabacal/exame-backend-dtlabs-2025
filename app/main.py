from fastapi import FastAPI 
from app.routes.user import router
from app.routes.server import router as server_router
from app.routes.sensor import router as sensor_router
from app.routes.health import router as health_router


app = FastAPI()

@app.get('/')
async def index():
    return "hello world"

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)

app.include_router(router)
app.include_router(server_router)
app.include_router(sensor_router)
app.include_router(health_router)

