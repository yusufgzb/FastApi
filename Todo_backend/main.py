from fastapi import Depends, FastAPI
from company.dependencies import get_token_header
import models
from db import engine

from routers import auth,todos, users
from company import companyapis, dependencies
app = FastAPI()



models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(
    companyapis.router,
    prefix="/companyapis",
    tags=["companyapis"],
    dependencies=[Depends(
                    dependencies.get_token_header) 
                        ],
    responses={418: {"description":"Internal USe Only"}}
)


# uvicorn main:app --reload
