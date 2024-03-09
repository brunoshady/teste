import uvicorn
from fastapi import FastAPI

from src import __version__
from src.handlers.users import users_router
from src.services.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User API",
    description="ZPE Service User API",
    version=__version__
)

app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=8080, workers=1, reload=True)
