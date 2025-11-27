# diary
Projeto de um diário pessoal.

# explicações

# 📔 API Diário Pessoal (Trabalho Prático)

API RESTful desenvolvida para gerenciamento de um diário pessoal. O sistema permite que usuários criem contas, façam login e gerenciem suas próprias anotações de forma segura e privada.

**Link da API Online:** [https://api-diario-chely.onrender.com/docs](https://api-diario-chely.onrender.com/docs)

---

## 🛠 Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Framework:** FastAPI
* **Banco de Dados:** Supabase (PostgreSQL)
* **Autenticação:** Supabase Auth (JWT)
* **Deploy:** Render
* **Segurança:** RLS (Row Level Security) - *Cada usuário vê apenas seus dados.*

---

## 🚀 Funcionalidades

* ✅ **Cadastro de Usuários:** Criação de conta com email e senha.
* ✅ **Autenticação:** Login seguro retornando Token de acesso (Bearer).
* ✅ **CRUD Completo:**
    * **Criar:** Adicionar nova página ao diário.
    * **Ler:** Listar todas as anotações do usuário logado.
    * **Detalhar:** Ler uma anotação específica por ID.
    * **Atualizar:** Editar o texto ou data de uma anotação.
    * **Excluir:** Deletar uma anotação.
* ✅ **Segurança:** O banco de dados bloqueia acesso a dados de outros usuários.

---

## 📚 Como Usar a API (Documentação)

A API possui documentação interativa (Swagger UI). Siga os passos abaixo para testar:

### 1. Criar Conta (Sign Up)
* Acesse a rota `POST /auth/signup`.
* Informe um email e senha.
* Clique em **Execute**.

### 2. Fazer Login (Obter Token)
* Acesse a rota `POST /auth/login`.
* Informe o email e senha cadastrados.
* Copie o código gigante que aparece no campo `"access_token"`.

### 3. Autenticar no Swagger 🔐
* No topo da página, clique no botão **Authorize** (cadeado).
* Cole o token copiado na caixa de texto.
* Clique em **Authorize** e depois **Close**.
* *Agora você está "logado" no sistema.*

### 4. Gerenciar o Diário
Agora você pode usar as rotas protegidas:
* **POST /notas:** Cria uma anotação (Ex: `{"data": "2025-11-27", "texto": "Hoje aprendi FastAPI"}`).
* **GET /notas:** Lista suas anotações.
* **PUT /notas/{id}:** Edita uma nota (Use o ID retornado na listagem).
* **DELETE /notas/{id}:** Apaga uma nota.

---

## 💻 Como Rodar Localmente

Se quiser rodar o projeto na sua máquina (vou deixar anotado pra eu não esquecer):

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/ChelyDev/diary.git](https://github.com/ChelyDev/diary.git)
    cd diary
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    Crie um arquivo `.env` na raiz e adicione suas chaves do Supabase:
    ```env
    SUPABASE_URL="sua_url_aqui"
    SUPABASE_KEY="sua_key_aqui"
    ```

5.  **Execute o servidor:**
    ```bash
    uvicorn app.main:app --reload
    ```
    Acesse em: `http://127.0.0.1:8000/docs`

---

## 📋 Estrutura do Banco de Dados (Supabase)

Tabela `diario`:
* `id`: int8 (Primary Key)
* `created_at`: timestamp
* `data`: date
* `texto`: text
* `user_id`: uuid (Foreign Key -> auth.users)

---

**Desenvolvido por Michely Costa Dantas**