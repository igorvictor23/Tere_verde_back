# Terê Verde - Backend API

Esta é a API RESTful desenvolvida para o projeto **Terê Verde**, um sistema focado na divulgação e gestão de eventos em parques naturais da cidade de Teresópolis. A aplicação atua como o núcleo lógico do sistema, gerenciando autenticação de administradores, persistência de dados de eventos, integração com serviços meteorológicos e um assistente virtual baseado em Inteligência Artificial.

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

O ecossistema do projeto foi construído utilizando **Python 3.12+** e ferramentas modernas para garantir alta performance, segurança e escalabilidade.

### Core & Framework
* **[FastAPI](https://fastapi.tiangolo.com/):** Framework web assíncrono de alto desempenho utilizado para o roteamento e construção da API.
* **[Uvicorn](https://www.uvicorn.org/):** Servidor ASGI super-rápido utilizado para rodar a aplicação FastAPI em produção e desenvolvimento.

### Banco de Dados & ORM
* **[SQLAlchemy](https://www.sqlalchemy.org/):** Mapeador Objeto-Relacional (ORM) utilizado para modelagem do banco de dados e execução de transações.
* **[psycopg2-binary](https://www.psycopg.org/):** Adaptador de banco de dados PostgreSQL para Python, garantindo comunicação estável com o banco relacional.

### Validação & Configuração
* **[Pydantic](https://docs.pydantic.dev/):** Utilizado para a validação rigorosa de dados de entrada e saída (Schemas).
* **[pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/):** Gerenciamento tipado de variáveis de ambiente, garantindo que o sistema não inicie sem as configurações críticas.
* **[email-validator](https://github.com/JoshData/python-email-validator):** Biblioteca de suporte ao Pydantic para validação robusta do formato de e-mails (`EmailStr`).

### Segurança & Autenticação
* **[PyJWT](https://pyjwt.readthedocs.io/):** Responsável pela criação e decodificação de JSON Web Tokens (JWT) para controle de sessão baseada em *Bearer Tokens*.
* **[pwdlib[bcrypt]](https://github.com/frankie567/pwdlib):** Utilizada para o hash seguro de senhas (criptografia unidirecional) e verificação de credenciais, utilizando o algoritmo Bcrypt.

### Integrações Externas (APIs)
* **[HTTPX](https://www.python-httpx.org/):** Cliente HTTP assíncrono utilizado para realizar requisições não-bloqueantes à API de clima externa (Open-Meteo).
* **[google-genai](https://pypi.org/project/google-genai/):** SDK oficial do Google utilizado para integrar o modelo **Gemini 2.5 Flash**, que alimenta o chatbot e atua como Guia Virtual da plataforma.

---

## 🏗️ Arquitetura e Boas Práticas Implementadas

O código foi estruturado seguindo princípios sólidos de engenharia de software e padrões de mercado:

* **Dependências Determinísticas (Reproducible Builds):** O projeto utiliza a ferramenta `uv` juntamente com o arquivo `uv.lock`. Isso trava as versões exatas de cada dependência (e sub-dependências), garantindo que o ambiente de produção e o ambiente de qualquer outro desenvolvedor sejam idênticos, eliminando quebras por atualizações inesperadas de bibliotecas.
* **Programação Assíncrona (`async/await`):** Chamadas a serviços de terceiros (como a API do Google Gemini e a API meteorológica) são realizadas de forma assíncrona, garantindo que a thread principal do servidor não seja bloqueada durante a espera por I/O da rede.
* **Segurança de Dados e Senhas:** As senhas dos administradores nunca são trafegadas ou armazenadas em texto plano. A criptografia ocorre na camada de serviço antes da persistência no banco.
* **Injeção de Dependências (Dependency Injection):** O acesso ao banco de dados é gerenciado por injeção (`get_db`). O uso de blocos `try/finally` com a instrução `yield` garante que a sessão do banco seja adequadamente fechada após cada requisição, prevenindo vazamento de memória e exaustão do *Connection Pool*.
* **Proteção de Variáveis Sensíveis (Fail-Fast):** Chaves de API e URLs de banco de dados são isolados através do arquivo `.env` e validados em tempo de execução pela classe `BaseSettings`. Se faltar alguma configuração crítica, a aplicação falha imediatamente ao iniciar, evitando comportamentos inesperados em produção.

---

## 🚀 Como Executar o Projeto Localmente

Siga o passo a passo abaixo para configurar o ambiente de desenvolvimento, inicializar o banco de dados e rodar a API.

### 1. Pré-requisitos
Certifique-se de ter instalado em sua máquina:
* Python 3.12 ou superior.
* Servidor PostgreSQL rodando localmente (ou em nuvem).
* Gerenciador de pacotes **[uv](https://docs.astral.sh/uv/)** instalado (extremamente rápido e gerencia o `uv.lock`).

### 2. Clonar o Repositório
```bash
git clone [https://github.com/seu-usuario/tere-verde-back.git](https://github.com/seu-usuario/tere-verde-back.git)
cd tere-verde-back
