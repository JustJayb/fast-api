from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
# from sqlalchemy_utils.types import ChoiceType

#conexao do banco
db = create_engine("sqlite:///banco.db")

#  Migrar o banco de dados

# criar a migracao: alembic revision --autogenerate -m "texto indicando a alteracao feita"
# executar a migracao: alembic upgrade head




#base do banco
Base = declarative_base()

#usuarios
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, autoincrement=True, primary_key=True)
    nome = Column("nome", String )
    email = Column("email", String,nullable=True)
    senha= Column("senha", String)
    ativo = Column("ativo", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True ,admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


#pedidos
class Pedido(Base):
    __tablename__ = "pedidos"

    # STATUS_PEDIDOS = (
    #     ("PENDENTE","PENDENTE"),
    #     ("CANCELADO","CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")  
    # )    status = Column("status", ChoiceType(choices=STATUS_PEDIDOS))

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    status = Column("status", String) # stutus pendente, cencelado e finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id")) 
    preco = Column("preco", Float)
    itens = relationship("ItemPedido", cascade="all, delete")
    # itens = 
    def __init__(self, usuario, status="PENDENTE", preco=0 ):
        self.usuario = usuario
        self.status = status
        self.preco = preco
            

    def calcular_preco(self):  
        #percorrer todos os itens do pedido   
        # somar todos os precos de todos os itens dos pedidos
        # editar no campo "preco" o valor final do preco do pedido
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)



class ItemPedido(Base):
     __tablename__ = "itens_pedido"

     id = Column("id", Integer, autoincrement=True, primary_key=True)
     quantidade = Column("quantidade", Integer)
     sabor = Column("sabor", String)
     tamanho = Column("tamanho", String)
     preco_unitario = Column("preco_unitario", Float)
     pedido = Column("pedido", ForeignKey("pedidos.id"))


     def __init__(self, quantidade, sabor, tamanho,preco_unitario,pedido ):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
 