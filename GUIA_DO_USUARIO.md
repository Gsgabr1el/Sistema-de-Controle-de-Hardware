# Guia do Usuário - AssetFlow
**Sistema de Controle de Ativos e Hardware**

Este guia descreve como acessar e utilizar todas as funcionalidades do sistema AssetFlow, desenvolvido para a disciplina de Prática Profissional em ADS (Mackenzie).

---

## 1. Como Acessar a Aplicação

A aplicação está disponível no seguinte endereço:
**URL:** https://assetflow.onrender.com

### Requisitos
* Navegador moderno (Chrome, Edge, Firefox).
* Conexão com a internet.

---

## 2. Instruções de Login

Ao acessar a URL, você será direcionado para a tela de login. O sistema possui um perfil de administrador pré-cadastrado e está pronto para o cadastro de novos ativos e colaboradores.

*   **Usuário:** `Admin`
*   **Senha:** `ejQTL0MV7Q0oChX17H8E`

> [!NOTE]
> O login utiliza autenticação segura com **JWT (JSON Web Token)**. Após o login, o sistema mantém sua sessão ativa localmente.

---

## 3. Navegação e Telas

O sistema é dividido em três módulos principais, acessíveis através da barra de navegação superior:

### 3.1. Gestão de Ativos (Home)
Esta é a tela principal onde você visualiza o resumo de inventário e a lista de equipamentos.

#### Funcionalidades:
*   **Dashboards:** Mostra o total de ativos e a quantidade por status (Disponíveis, Em Uso, Manutenção, Descarte).
*   **Cadastrar Novo Ativo:** Clique no botão verde "+ Novo Ativo" para adicionar um equipamento informando:
    *   Código do Ativo (ID numérico)
    *   Nome (Ex: Notebook Dell)
    *   Descrição (Ex: i7 16GB)
*   **Busca:** Utilize a barra de busca para pesquisar ativos por **nome** ou **código**.
*   **Ações (Entrega/Devolução/Manutenção):**
    *   **Entregar:** Se o ativo estiver "Disponível", clique em "Entregar" para vinculá-lo a um colaborador (informando o ID do funcionário).
    *   **Devolver:** Se o ativo estiver "Em Uso", clique em "Devolver" para retornar o equipamento ao estoque, podendo escolher o novo status (Disponível, Manutenção ou Descarte).
    *   **Concluir Manutenção:** Para ativos com o status "Manutenção", clique no botão verde que aparece na tabela para torná-lo "Disponível" novamente de forma rápida após o reparo.
*   **Vínculo de Responsável:** A tabela de ativos exibe o nome do colaborador que está com o equipamento em tempo real.

### 3.2. Colaboradores
Exibe a lista de todos os funcionários cadastrados na empresa e permite sua gestão completa.

#### Funcionalidades:
*   **Listagem Completa:** Exibe ID, Nome, E-mail e Departamento.
*   **Visualização de Ativos:** Uma coluna exclusiva mostra todos os equipamentos que estão atualmente sob a responsabilidade de cada colaborador (Código e Nome do Ativo).
*   **Cadastrar Novo Colaborador:** Clique em "+ Novo Colaborador" para adicionar um novo registro.
*   **Editar Registro:** Clique no ícone de **Lápis** para alterar Nome, E-mail ou Departamento de um funcionário.
*   **Excluir (Regra de Segurança):** Clique no ícone de **Lixeira** para remover um colaborador.
    *   **Importante:** O sistema protege a integridade dos dados e **impede** a exclusão se o funcionário ainda possuir ativos vinculados. É necessário registrar a devolução dos ativos antes de prosseguir com a exclusão.

### 3.3. Movimentações (Histórico)
Registra todas as ações realizadas no sistema para fins de auditoria.

#### Funcionalidades:
*   **Rastreabilidade:** Cada linha mostra a Data/Hora, o tipo de operação (Entrega/Devolução), o Ativo envolvido e o Colaborador responsável.

---

## 4. Persistência de Dados
Todas as operações de alteração (Cadastro, Entrega, Devolução) são gravadas em tempo real no banco de dados **SQLite**.

### Como validar a persistência:
1. Cadastre um novo ativo.
2. Saia do sistema (Logout).
3. Entre novamente.
4. O ativo continuará listado, confirmando que os dados não foram perdidos.

---

## 5. Suporte
Em caso de dúvidas técnicas, consulte os arquivos `README.md` e `main.py` no repositório de código-fonte.

---
**Grupo 43 - Mackenzie 2026**
