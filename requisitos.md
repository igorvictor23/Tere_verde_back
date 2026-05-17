# Requisitos Funcionais 

* **RF01** - O sistema deve permitir o cadastro de novos administradores, exigindo nome, e-mail válido e senha
* **RF02** - O sistema deve autenticar os administradores através de e-mail e senha, retornando um token de acesso seguro para a sessão
* **RF03** - O sistema deve permitir a listagem de todos os administradores cadastrados, exibindo suas informações básicas e o status de atividade (restrito ao Super Administrador)
* **RF04** - O sistema deve permitir que administradores autenticados cadastrem, atualizem (título, descrição, data, parque) e excluam eventos na plataforma.
* **RF05** - O sistema deve fornecer uma listagem pública de todos os eventos cadastrados para que o front-end possa exibi-los aos visitantes sem a necessidade de login.
* **RF06** - O sistema deve permitir que usuários visitantes se inscrevam nos eventos públicos informando um e-mail válido.
* **RF07** - O sistema deve exibir feedbacks visuais (Toasts) informando o sucesso ou falha em ações chave, como criar/atualizar eventos ou ao concluir uma inscrição.
* **RF08** - O sistema deve exibir um modal de confirmação (pergunta de segurança) antes de executar a exclusão definitiva de qualquer evento ou registro.
* **RF09** - O sistema deve receber uma data específica, consultar uma API externa e processar a resposta para retornar a temperatura máxima e o emoji representativo do clima daquele dia.
* **RF10** - O sistema deve disponibilizar um endpoint de chat interativo para receber mensagens dos usuários e devolver respostas geradas pelo modelo de Inteligência Artificial.
* **RF11** - O sistema deve registrar automaticamente um histórico (Log) das operações realizadas, contendo o tipo de ação, o administrador responsável, a data/hora exata e o evento modificado.

---

# Requisitos Não Funcionais 

* **RNF01** (Segurança) - A proteção das senhas deve ser garantida realizando a criptografia unidirecional (hash) através do algoritmo Bcrypt antes da persistência no banco de dados.
* **RNF02** (Segurança) - A proteção e o controle de sessão das rotas fechadas da API devem ser realizados obrigatoriamente através de JSON Web Tokens (JWT).
* **RNF03** (Segurança) - O back-end deve implementar políticas de Cross-Origin Resource Sharing (CORS) para permitir a comunicação segura com o front-end hospedado em domínios externos.
* **RNF04** (Desempenho) - A comunicação do sistema com serviços de terceiros (API meteorológica Open-Meteo e IA Google Gemini) deve ser executada de forma assíncrona, evitando o bloqueio da thread principal do servidor (I/O não-bloqueante).
* **RNF05** (Desempenho) - O sistema deve injetar sessões do banco de dados utilizando blocos de tentativa/finalização (`try/finally`), garantindo o encerramento da conexão após cada requisição para prevenir vazamento de memória e exaustão do pool de conexões.
* **RNF06** (Desempenho) - A interface de usuário (JavaScript) deve implementar validações de nulidade e encapsulamento na manipulação do DOM para garantir que a ausência de um elemento em determinada página não cause erros fatais (Graceful Degradation).
* **RNF07** (Confiabilidade) - O sistema deve utilizar o PostgreSQL como banco de dados relacional e ser capaz de criar toda a sua estrutura de tabelas automaticamente via ORM (SQLAlchemy) durante a inicialização.
* **RNF08** (Confiabilidade) - O sistema deve validar rigorosamente os tipos de dados e os formatos (ex: estrutura de E-mail) já na camada de transporte (via Pydantic), rejeitando payloads malformados com erro 422 antes de acionar o banco de dados.
* **RNF09** (Confiabilidade) - O back-end deve validar a presença de variáveis de ambiente críticas (chaves de API, segredos JWT, URL do banco) no momento da inicialização do servidor, abortando a execução imediatamente caso alguma configuração falte.
* **RNF10** (Manutenibilidade) - O gerenciamento de dependências do back-end deve ser feito através de padrões modernos (pyproject.toml e arquivos .lock), garantindo que o ambiente seja idêntico em qualquer máquina de desenvolvimento ou servidor de produção.
* **RNF11** (Manutenibilidade) - O sistema deve ser arquitetado de forma desacoplada, permitindo que a API (Back-end) rode em plataformas como o Render, enquanto os arquivos estáticos (Front-end) sejam distribuídos via CDN/servidores estáticos como o GitHub Pages, utilizando o protocolo HTTPS.

---

# Regras de Negócio

* **RN01** - O cadastro e a realização de eventos são restritos aos domínios: "PARNASO", "Três Picos" ou "Montanhas de Teresópolis".
* **RN02** - É proibido o cadastro ou a alteração de eventos para datas retroativas (no passado).
* **RN03** - O Guia Virtual (IA) atua exclusivamente no escopo de ecoturismo e parques de Teresópolis, devendo recusar outros assuntos.
* **RN04** - Apenas o perfil "Super Administrador" (super = True) possui permissão para acessar o histórico de auditoria (Logs) e gerenciar a lista de administradores.
* **RN05** - Toda manipulação da base de eventos (Criação, Atualização, Exclusão) exige registro obrigatório em Log, vinculando o usuário, a ação e o horário exato.
* **RN06** - A inscrição de visitantes em eventos públicos exige apenas o fornecimento de um e-mail válido, dispensando a criação de contas ou senhas.
* **RN07** - Administradores removidos da equipe sofrem inativação lógica (`ativo = False`), impedindo a exclusão física do banco para preservar a integridade do histórico de auditoria.