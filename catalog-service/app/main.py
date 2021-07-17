import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from app.routers import product_router, tech_spec_router, security_router, sync_router
from app.database.models import Base
from app.database.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/security/token')

app.include_router(product_router.router, dependencies=[
                   Depends(oauth2_scheme)])
app.include_router(tech_spec_router.router,
                   dependencies=[Depends(oauth2_scheme)])
app.include_router(sync_router.router, dependencies=[Depends(oauth2_scheme)])
app.include_router(security_router.router)


@app.get('/')
async def home():
    return {'message': 'Welcome to the Catalog Service'}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, workers=4)
