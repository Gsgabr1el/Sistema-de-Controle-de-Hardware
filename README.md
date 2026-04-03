# AssetFlow
## Grupo 43

## Sistema-de-Controle-de-Hardware

## Grupo 43

Sistema acadêmico para controle de hardware/ativos de uma empresa, desenvolvido com FastAPI, SQLAlchemy e SQLite.


## Observações

- O banco de dados usado é SQLite local.
- O arquivo do banco é criado automaticamente em `backend/database.db`.
- Sistema com foco em simplicidade e funcionamento especifico.


## IMPORTANTE ##
## Arquivo do banco de dados

O sistema gera automaticamente um arquivo local para armazenar os dados do banco SQLite. Esse arquivo não está incluído no `.gitignore`, então CUIDADO ao fazer commits!

Ele guarda todas as informações cadastradas e transacionadas no sistema, como usuários, colaboradores, ativos e movimentações. Se esse arquivo for apagado, todos os dados armazenados nele também serão perdidos. Ao executar o sistema novamente, um novo arquivo de banco será criado automaticamente.






## Objetivo

O sistema organiza o controle de equipamentos da empresa, permitindo:

- Cadastrar e listar ativos;
- Vincular um ativo a um colaborador;
- Registrar devolução, manutenção ou descarte;
- Acompanhar o histórico de movimentações;
- Autenticar o usuário administrador com token.

## Tecnologias utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT para autenticação

## Como o sistema funciona

Ao iniciar a aplicação, o backend cria automaticamente as tabelas do banco e também cadastra:

- 40 colaboradores fictícios;
- Um usuário administrador (Que é o único responsável pelo sistema).

O fluxo principal é:

1. Fazer login com as credencias do administrador **(Que a empresa fornecera "exclusivamente para ele")**;
2. Cadastrar um ativo ou mais ativos;
3. Entregar o ativo para um colaborador;
4. Registrar a devolução, manutenção ou descarte;
5. Consultar o histórico de movimentações.

## Estrutura do banco de dados

### `usuarios`
Armazena os usuários responsáveis pelo sistema.

- `id`
- `username`
- `senha_hash`

### `colaboradores`
Armazena os colaboradores da empresa.

- `id`
- `nome`
- `email`
- `departamento`

### `ativos`
Armazena os equipamentos controlados pelo sistema.

- `id`
- `colaborador_id`
- `codigo_ativo`
- `nome`
- `descricao`
- `status`

### `movimentacoes`
Armazena o histórico de entrega, devolução e manutenção.

- `id`
- `data_hora`
- `tipo`
- `ativo_id`
- `colaborador_id`
- `codigo_ativo`

## Funcionalidades

### Login
Autentica o usuário administrador e retorna um token JWT para uso nas rotas protegidas.

### Cadastro de ativos
Permite criar um novo ativo com nome, código e descrição.

### Busca de ativos
Permite buscar ativos pelo nome ou pelo código.

### Entrega de ativo
Vincula um ativo a um colaborador e altera seu status para `EM_USO`.

### Devolução / manutenção
 Registra a devolução do ativo e permite alterar o status para `DISPONIVEL`, `MANUTENCAO` ou `DESCARTE`.

### Listagem de colaboradores
Retorna todos os colaboradores cadastrados no banco.

### Consulta de movimentações
Retorna o histórico completo das movimentações dos ativos.

## Endpoints

### `POST /login`
Realiza o login do responsável pelo sistema.

Parâmetros:
- `username`
- `senha`

Os dados devem ser enviados no corpo da requisição.

Retorno:
- `access_token`

### `POST /ativos`
Cria um novo ativo.

Parâmetros:
- `nome`
- `codigo_ativo`
- `descricao`

Os dados devem ser enviados no corpo da requisição.

### `POST /ativos/busca`
Busca ativos por nome ou código.

Parâmetros:
- `termo` 

Os dados devem ser enviados no corpo da requisição.

### `GET /ativos`
Lista todos os ativos.

Requer token Bearer.

### `POST /entrega`
Registra a entrega de um ativo para um colaborador.

Parâmetros:
- `codigo_ativo`
- `colaborador_id`

Os dados devem ser enviados no corpo da requisição.

### `POST /devolucao`
 Registra a devolução, manutenção ou descarte de um ativo.

Parâmetros:
- `codigo_ativo`
- `status`

Os dados devem ser enviados no corpo da requisição.

### `GET /colaboradores`
Lista todos os colaboradores.

### `POST /colaboradores/busca`
Busca um colaborador pelo ID.

Os dados devem ser enviados no corpo da requisição.

### `GET /movimentacoes`
Lista todas as movimentações registradas.

Observação: exceto a rota `POST /login`, todas as demais rotas exigem token JWT no cabeçalho `Authorization`.

## Como executar o backend

### No Linux

1. Acesse a pasta do backend:

```bash
cd backend
```

2. Instale as dependências do projeto:

```bash
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt]
```

3. Inicie o servidor FastAPI:

```bash
uvicorn main:app --reload
```

4. Acesse a documentação interativa:

- Swagger: `http://127.0.0.1:8000/docs`

### No Windows

1. Acesse a pasta do backend:

```bat
cd backend
```

2. Crie o ambiente virtual:

```bat
python -m venv venv
```

3. Ative o ambiente virtual:

No PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

No CMD:

```bat
venv\Scripts\activate.bat
```

4. Instale as dependências do projeto:

```bat
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt]
```

5. Inicie o servidor FastAPI:

```bat
uvicorn main:app --reload
```

6. Acesse a documentação interativa:

- Swagger: `http://127.0.0.1:8000/docs`

## Como testar o backend no FastAPI

### 1. Fazer login
Abra `POST /login` no Swagger e envie:

```json
{
  "username": "Admin",
  "senha": "ejQTL0MV7Q0oChX17H8E"
}
```

Se estiver correto, a resposta será um token JWT.

### 2. Usar o token nas rotas protegidas
Na rota `GET /ativos`, clique em **Authorize** e informe:

```text
TOKEN_AQUI
```

### 3. Testar cadastro de ativo
Envie um `POST /ativos` com dados como:

```json
{
  "nome": "Notebook Dell",
  "codigo_ativo": 1001,
  "descricao": "Notebook administrativo"
}
```

### 4. Testar entrega
Use `POST /entrega` com:

```json
{
  "codigo_ativo": 1001,
  "colaborador_id": 1
}
```

### 5. Testar devolução
Use `POST /devolucao` com um status válido, por exemplo:

```json
{
  "codigo_ativo": 1001,
  "status": "DISPONIVEL"
}
```

Ou, se quiser mandar para manutenção:

```json
{
  "codigo_ativo": 1001,
  "status": "MANUTENCAO"
}
```

### 6. Consultar colaboradores e movimentações
Teste as rotas:

- `GET /colaboradores`
- `POST /colaboradores/busca`
- `GET /movimentacoes`

## Respostas de erro

O projeto já retorna erros HTTP mais corretos para facilitar o uso da API.

- `404` quando algo não é encontrado
- `400` quando a requisição é inválida
- `401` quando a autenticação falha
- `409` quando há conflito de estado