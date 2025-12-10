# ✅ API de Tarefas – Flask

API RESTful para gerenciamento de tarefas, desenvolvida em Python utilizando Flask, SQLAlchemy e banco de dados SQLite. O projeto permite criar, listar, atualizar, filtrar e remover tarefas, com validação de dados e retorno padronizado via HTTP. Este projeto foi desenvolvido com foco em aprendizado prático de Back-end e APIs REST.

🚀 Tecnologias Utilizadas  
Python  
Flask  
Flask-SQLAlchemy  
SQLite  
Git & GitHub  

📦 Instalação e Execução Local (Sem Ambiente Virtual)  
⚠️ Este projeto não utiliza ambiente virtual (venv). As dependências serão instaladas diretamente no Python global da máquina.

💻 Comandos para rodar o projeto localmente:

git clone https://github.com/EmersonPO25/api-de-tarefas-python-flask.git  
cd api-de-tarefas-python-flask  
pip install -r requirements.txt  
pip install -r requirements.txt --user  
python app.py  

🌐 A API ficará disponível em:  
http://127.0.0.1:5000  

📌 Rotas disponíveis da API:

➕ Criar tarefa  
POST /tasks  
Body:  
{
  "title": "Estudando programação",
  "description": "Criei a minha primeira API"
}

📄 Listar todas as tarefas  
GET /tasks  

✅ Filtrar tarefas por status  
GET /tasks?done=true  
GET /tasks?done=false  

🔍 Buscar tarefa por ID  
GET /tasks/{id}  

✏️ Atualizar uma tarefa  
PUT /tasks/{id}  
Body:  
{
  "done": true
}

🗑️ Deletar uma tarefa  
DELETE /tasks/{id}  

✅ Funcionalidades implementadas: 
- CRUD completo de tarefas
- validação de dados de entrada
- filtro por status, tratamento de erros com respostas HTTP adequadas
- banco de dados local com SQLite.

🎯 Objetivo do projeto:
- demonstrar na prática o desenvolvimento de APIs REST
- organização de código Back-end
- integração com banco de dados usando ORM (SQLAlchemy).

👨‍💻 Autor: Emerson Oliveira  
GitHub: https://github.com/EmersonPO25
