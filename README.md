# README - Como Rodar o Projeto com Docker e FastAPI

## Requisitos
Antes de iniciar, certifique-se de ter os seguintes requisitos instalados:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.10+](https://www.python.org/downloads/)

## Configuração do Ambiente
1. **Criação do ambiente virtual (opcional, caso rode sem Docker)**

   Se quiser rodar o projeto localmente sem Docker, crie e ative um ambiente virtual:

   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configurar o arquivo `.env`**

   Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis:

   ```env
   POSTGRES_USER=seu_usuario
   POSTGRES_PASSWORD=sua_senha
   POSTGRES_DB=seu_banco
   DB_URL=postgresql://seu_usuario:sua_senha@meu-banco:5432/seu_banco
   ```

   **⚠️ NÃO suba o `.env` para o Git!**

   Para evitar isso, adicione ao `.gitignore`:
   ```sh
   echo ".env" >> .gitignore
   ```
   Crie um `.env.example` para referência:
   ```env
   POSTGRES_USER=exemplo_usuario
   POSTGRES_PASSWORD=exemplo_senha
   POSTGRES_DB=exemplo_banco
   DB_URL=postgresql://exemplo_usuario:exemplo_senha@meu-banco:5432/exemplo_banco
   ```

## Rodando o Projeto com Docker

### 1. Construir e Iniciar os Contêineres

Execute o seguinte comando no terminal, na raiz do projeto:

```sh
docker-compose up --build
```

Isso irá:
- Criar e iniciar um contêiner para o PostgreSQL.
- Criar e iniciar um contêiner para a aplicação FastAPI.
- Aplicar as migrações do banco de dados usando `alembic upgrade head`.
- Rodar o servidor FastAPI com `uvicorn`.

### 2. Verificar se os Contêineres Estão Rodando

Para conferir os contêineres em execução, use:

```sh
docker ps
```

Você deve ver os contêineres `meu-banco` (PostgreSQL) e o contêiner da aplicação rodando.

### 3. Acessar a Aplicação

A API estará disponível em:

- Documentação interativa Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 4. Parar os Contêineres

Para parar os contêineres sem removê-los, use:

```sh
docker-compose down
```

Se quiser remover os volumes junto com os contêineres:

```sh
docker-compose down -v
```

## Estrutura do Projeto

```
📂 meu_projeto
├── 📂 app
│   ├── 📂 models
│   ├── 📂 routes
│   ├── 📂 schemas
│   ├── 📜 main.py
├── 📜 Dockerfile
├── 📜 docker-compose.yml
├── 📜 requirements.txt
├── 📜 alembic.ini
├── 📂 alembic
│   ├── 📜 env.py
│   ├── 📂 versions
├── 📜 .env.example
```

Agora seu projeto está pronto para rodar com Docker! 🚀

