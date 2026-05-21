# AssetFlow
## Grupo 43

Sistema acadêmico para controle de ativos (hardware/software), desenvolvido com FastAPI, SQLAlchemy e SQLite.


## Observações

- O banco de dados usado é SQLite local.
- O arquivo do banco é criado automaticamente em `backend/database.db`.
- Sistema com foco em simplicidade e funcionamento especifico.


## Persistência de Dados

O banco de dados (SQLite) é gerado automaticamente no arquivo local `backend/database.db`. Por questões de segurança e boas práticas, este arquivo foi explicitamente adicionado ao `.gitignore` para evitar envio acidental de dados ou credenciais ao repositório.

Caso o arquivo `database.db` seja excluído do ambiente local, o sistema recriará automaticamente a estrutura de tabelas e o usuário administrador padrão na próxima execução inicial do servidor.

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

Ao iniciar a aplicação pela primeira vez, o backend cria automaticamente as tabelas do banco e um usuário administrador padrão. O sistema inicia sem colaboradores pré-cadastrados para permitir uma demonstração limpa das funcionalidades de cadastro.

O fluxo principal é:

1. Fazer login com as credencias do administrador;
2. Cadastrar colaboradores e ativos;
3. Gerenciar o vínculo de ativos entre empresa e funcionários;
4. Acompanhar movimentações e manutenções;
5. Utilizar as travas de segurança para evitar exclusões indevidas.

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

### Gestão de Colaboradores (CRUD)
Permite cadastrar, listar, editar e excluir funcionários. Possui trava de segurança que impede a exclusão de colaboradores com ativos em posse.

### Gestão de Ativos
Controle total sobre equipamentos, incluindo busca rápida, vinculação a responsáveis e histórico de estado.

### Controle de Manutenção
Fluxo simplificado para enviar equipamentos para reparo e retorná-los ao estoque com um único clique.

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

### Instalação (Windows/Linux)

1. Verifique a versão do Python no seu sistema:
```bash
python --version
```
Este projeto obrigatoriamente requer Python 3.10 ou superior.

2. Se necessario crie e ative um ambiente virtual:

python -m venv .venv
source .venv/bin/activate


3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Inicie o servidor (da pasta raiz do projeto):
```bash
PYTHONPATH=backend python -m uvicorn backend.main:app --reload
```

5. Acesse no navegador:
- Aplicação: `http://localhost:8000`
- Documentação API (Swagger): `http://localhost:8000/docs`

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