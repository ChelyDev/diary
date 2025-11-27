import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from supabase import create_client, Client
from dotenv import load_dotenv

#Carrega as variáveis de ambiente (localmente)
load_dotenv()

#CONFIGURAÇÃO 
#Pega as chaves do ambiente (funciona tanto no PC quanto no Render)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

#cliente padrão (usado apenas para login/signup inicial)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(
    title="API Diário Pessoal",
    description="API com Autenticação e RLS via Supabase. Desenvolvida para trabalho prático.",
    version="2.0.0"
)

#Esquema de segurança para pegar o Token Bearer do cabeçalho
security = HTTPBearer()

#MODELOS (PYDANTIC)

class UserAuth(BaseModel):
    email: str
    password: str

class NotaSchema(BaseModel):
    data: str  
    texto: str

class NotaDB(NotaSchema):
    id: int
    created_at: str
    user_id: str  #ID do dono da nota

#DEPENDÊNCIA DE SEGURANÇA
# Essa função pega o Token do usuário e cria um cliente Supabase específico para ele.
# Isso garante que as Regras de Segurança (RLS) funcionem.
def get_user_supabase(cred: HTTPAuthorizationCredentials = Depends(security)):
    token = cred.credentials
    try:
        #Cria um cliente novo e loga ele com o token recebido
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        client.auth.set_session(access_token=token, refresh_token=token)
        return client
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

#ROTAS DE AUTENTICAÇÃO (Públicas)

@app.post("/auth/signup", summary="Cria um novo usuário")
def signup(user: UserAuth):
    try:
        response = supabase_admin.auth.sign_up({
            "email": user.email, 
            "password": user.password
        })
        if not response.user:
            raise HTTPException(status_code=400, detail="Erro ao criar usuário")
        return {"msg": "Usuário criado com sucesso!", "user_id": response.user.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login", summary="Faz login e retorna o Token de acesso")
def login(user: UserAuth):
    try:
        response = supabase_admin.auth.sign_in_with_password({
            "email": user.email, 
            "password": user.password
        })
        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "user_email": response.user.email
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

#ROTAS DO DIÁRIO (Protegidas)
#Todas exigem estar logado

@app.get("/notas", response_model=List[NotaDB], summary="Lista apenas as notas do usuário logado")
def listar_notas(client: Client = Depends(get_user_supabase)):
    response = client.table("diario").select("*").execute()
    return response.data

@app.get("/notas/{nota_id}", response_model=NotaDB)
def buscar_nota(nota_id: int, client: Client = Depends(get_user_supabase)):
    response = client.table("diario").select("*").eq("id", nota_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Nota não encontrada")
    return response.data[0]

@app.post("/notas", status_code=201, response_model=NotaDB)
def criar_nota(nota: NotaSchema, client: Client = Depends(get_user_supabase)):
    try:
        #O user_id é preenchido automaticamente pelo banco (default auth.uid())
        response = client.table("diario").insert({
            "data": nota.data,
            "texto": nota.texto
        }).execute()
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/notas/{nota_id}", response_model=NotaDB)
def atualizar_nota(nota_id: int, nota: NotaSchema, client: Client = Depends(get_user_supabase)):
    response = client.table("diario").update({
        "data": nota.data,
        "texto": nota.texto
    }).eq("id", nota_id).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Nota não encontrada ou permissão negada")
    return response.data[0]

@app.delete("/notas/{nota_id}", status_code=204)
def deletar_nota(nota_id: int, client: Client = Depends(get_user_supabase)):
    client.table("diario").delete().eq("id", nota_id).execute()
    return None