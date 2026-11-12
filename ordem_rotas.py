from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencias import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from models import Pedido, Usuario, ItemPedido
from typing import List
ordem_rota = APIRouter(prefix="/pedidos", tags=["Pedidos"],  dependencies=[Depends(verificar_token)])

@ordem_rota.get("/")
async def pedidos():
    """
    Essa é a rota padrao de pedidos do sistema. todas as rotas dos pedidos precisam de autenticação
    """
    return {"mensagem": "Você acessou a rota de pedidos"}

@ordem_rota.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao) ): 
    novo_pedido = Pedido(usuario = pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso {novo_pedido.id}"}


@ordem_rota.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token) ):
    #usuario.admin = True
    #usuario.id = pedido.usuario
    pedido = session.query(Pedido).filter(Pedido.id== id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400 , detail="pedido nao encontrado")

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer o cancelamento")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"pedido {pedido.id} cancelado com sucesso",
        "pedido": pedido
    } 

@ordem_rota.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token) ):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer o cancelamento")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }
#adicionar o item no pedido
@ordem_rota.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema: ItemPedidoSchema,session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido: 
        raise HTTPException(status_code=400, detail="pedido n existe")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, 
                             item_pedido_schema.preco_unitario, id_pedido)
    
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido":  pedido.preco
    }
#remover o item no pedido
@ordem_rota.post("/pedido/remover-item/{id_item_pedido}")
async def adicionar_item_pedido(id_item_pedido: int, 
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not item_pedido: 
        raise HTTPException(status_code=400, detail="item no pedido n existe")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensagem": "Item removido com sucesso",
        "quantidade itens pedido": len(pedido.itens),
        "pedido": pedido
    } 

# finalizar um pedido
@ordem_rota.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token) ):
    #usuario.admin = True
    #usuario.id = pedido.usuario
    pedido = session.query(Pedido).filter(Pedido.id== id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400 , detail="pedido nao encontrado")

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer o cancelamento")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "mensagem": f"pedido {pedido.id} finalizado com sucesso",
        "pedido": pedido
    } 


# visualizar 1 pedido 

@ordem_rota.get("/pedido/{id_pedido}", response_model=ResponsePedidoSchema)
async def visualizar_pedido(id_pedido:  int,session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token) ):
        pedido = session.query(Pedido).filter(Pedido.id== id_pedido).first()
        if not pedido:
            raise HTTPException(status_code=400 , detail="pedido nao encontrado")
    
        if not usuario.admin and usuario.id != pedido.usuario:
            raise HTTPException(status_code=401, detail="Você não tem autorização para fazer o cancelamento")
        return {
                "mensagem": f"pedido {pedido.id} finalizado com sucesso",
                "quantidade_itens_pedido": len(pedido.itens),
                "pedido": pedido
            } 
        


# visualizar todos os pedidos de 1 usuário 

@ordem_rota.get("/listar/pedidos-usuario", response_model=List[ResponsePedidoSchema])
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token) ):
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return pedidos