from fastapi import Depends, HTTPException
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import  Usuario
from jose import jwt, JWTError
from main import CHAVE_SECRETA, ALGORITIMO, oauth2_schema


def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, CHAVE_SECRETA, ALGORITIMO)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")


    # verificar se o tolken é valido
    # extrair o ID do usuario do token
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario    





# Session = sessionmaker(bind= db)
#     session = Session()