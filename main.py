from fastapi import FastAPI
from routers import recommend

app = FastAPI()
app.include_router(recommend.router)

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8080)
