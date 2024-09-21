from app.core.config import settings
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base  # Importa a Base com os modelos
# from app.core.auth import get_current_user
from app.api.api_v1.vehicles import router


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configurações CORS (Cross-Origin Resource Sharing)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Em produção, defina domínios específicos
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# Inclui o roteador principal da API (com autenticação/authorization)
# app.include_router(router, prefix=settings.API_V1_STR)



# # Exemplo de rota protegida por autenticação
# @app.get("/secure-data", dependencies=[Depends(get_current_user)])
# async def get_secure_data():
#     return {"message": "This is a protected route. User is authenticated."}



app.include_router(router, prefix="/vehicles", tags=["Vehicles"])
