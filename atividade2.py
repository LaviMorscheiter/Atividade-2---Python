from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Atividade 2 - API RESTful de Clientes", description="API RESTful para gerenciamento de clientes", version="1.0.0")

banco_clientes = {}

class ClientePost(BaseModel):
    nome: str
    sobrenome: str
    
class ClientePut(BaseModel):
    _id: str
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    
class ClienteDelete(BaseModel):
    _id: str
    
@app.post("/clientes", status_code=status.HTTP_200_OK)
def cadastrar_cliente(cliente: ClientePost):
    novo_id = str(uuid.uuid4().int)[:9]
    banco_clientes[novo_id]= {
        "_id": novo_id,
        "nome": cliente.nome,
        "sobrenome": cliente.sobrenome
    }
    return Response(status_code=status.HTTP_200_OK)

@app.put("/clientes")
def alterar_cliente(cliente: ClientePut):
    if cliente._id in banco_clientes:
        if cliente.nome is not None:
            banco_clientes[cliente._id]["nome"] = cliente.nome
        if cliente.sobrenome is not None:
            banco_clientes[cliente._id]["sobrenome"] = cliente.sobrenome
        return banco_clientes[cliente._id]
    return Response(content= '{"erro":"Cliente não encontrado"}', status_code=status.HTTP_404_NOT_FOUND)

@app.delete("/clientes", status_code=status.HTTP_200_OK)
def deletar_cliente(cliente: ClienteDelete):
    if cliente._id in banco_clientes:
        del banco_clientes[cliente._id]
        return Response(status_code=status.HTTP_200_OK)
    return Response(content= '{"erro":"Cliente não encontrado"}', status_code=status.HTTP_404_NOT_FOUND)

@app.get("/clientes")
def listar_clientes():
    return list(banco_clientes.values())