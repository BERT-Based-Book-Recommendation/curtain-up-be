from fastapi import FastAPI
from routers import test

app = FastAPI()
app.include_router(test.router)

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8080)
