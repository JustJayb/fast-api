# para rodar o codigo executar no terminal: ->  uvicorn main:app --reload

from fastapi import FastAPI
from passlib.context import CryptContext 
from dotenv import load_dotenv
import os 
from fastapi.security import OAuth2PasswordBearer

#chave secreta dentro do .env
load_dotenv()

CHAVE_SECRETA = os.getenv("CHAVE_SECRETA")
ALGORITIMO = os.getenv("ALGORITIMO") 
TOKEN_EXPIRA_EM= int(os.getenv("TOKEN_EXPIRA_EM") )

app = FastAPI()
#criptografar a senha
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")


from autenticacao_rotas import autent_rota
from ordem_rotas import ordem_rota

app.include_router(autent_rota)
app.include_router(ordem_rota)







#endpoint:
#/ordens  

