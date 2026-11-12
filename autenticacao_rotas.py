from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import Usuario
from dependencias import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITIMO, TOKEN_EXPIRA_EM, CHAVE_SECRETA
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

autent_rota = APIRouter(prefix="/auth", tags=["Autenticação"])

 #JWT
def criar_token(id_usuario, duracao_token=timedelta(minutes=TOKEN_EXPIRA_EM)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario),"exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, CHAVE_SECRETA, ALGORITIMO)
    return jwt_codificado



 

def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario




@autent_rota.get("/")
async def home():
    """
    Essa é a rota padrao de autenticação do sistema
    """
    return {"mensagem": "Você acessou a rota padrão de autenticação", "autenticado": False}

@autent_rota.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao) ):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        # ja tem um usuario com esse email
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return{"mensagem": f"usuario cadastrado com sucesso {usuario_schema.email}"}



    #session.close()


# login -> email e senha -> token JWT
@autent_rota.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else: 
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return{
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }

# Login no Docs "Authorize"
@autent_rota.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends ()  , session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    else: 
        access_token = criar_token(usuario.id)
        return{
            "access_token": access_token,           
            "token_type": "Bearer"
        }




    
        # JWT Bearer

        # headers = {"Access-Token": "Bearer token"}

@autent_rota.get("/refresh")
async def usar_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return{
            "access_token": access_token,
            "token_type": "Bearer"
        }





