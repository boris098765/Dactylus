import os
from pathlib import Path
from fastapi import FastAPI

from app.api.routes import category
from app.infra.db import init_db

app = FastAPI()


@app.on_event("startup")
def startup():
    db_path = Path(
        os.getenv("DATABASE_URL", "").replace("sqlite:///", "")
    )
    if db_path.parent:
        db_path.parent.mkdir(parents=True, exist_ok=True)
    init_db()


app.include_router(category.router)