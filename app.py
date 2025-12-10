from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Config do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_itens.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        """Converte a Task em dicionário para resposta JSON."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done
        }


# Cria as tabelas no banco
with app.app_context():
    db.create_all()


# ---------- Funções de validação ----------

def get_json_data():
    """pega o JSON da requisição. Se não tiver nada, retorna dict vazio."""
    data = request.get_json(silent=True)
    if data is None:
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def validate_task_payload(data, partial=False):
    """
    Valida os dados da task.
    True: usado no PUT para atualização parcial.
    False: usado no POST para criação - tem que ter title.
    """

    errors = {}

    # Validação do título
    title = data.get('title')
    if not partial or ('title' in data):
        if not isinstance(title, str) or not title.strip():
            errors['title'] = 'title é obrigatório e deve ser uma string não vazia.'

    # Validação da descrição
    if 'description' in data:
        if data['description'] is not None and not isinstance(data['description'], str):
            errors['description'] = 'description deve ser uma string ou null.'

    # Validação do done (se enviado)
    if 'done' in data:
        # Aceita True/False, 0/1, "true"/"false"
        value = data['done']
        if isinstance(value, str):
            if value.lower() not in ('true', 'false', '0', '1'):
                errors['done'] = 'done deve ser booleano (True/False) ou equivalente.'
        elif not isinstance(value, (bool, int)):
            errors['done'] = 'done deve ser booleano (True/False) ou 0/1.'

    return errors


def parse_done_value(value):
    """Converte o parâmetro done (string) em booleano."""
    if value is None:
        return None
    value = value.lower()
    if value in ('true', '1', 't', 'yes', 'y'):
        return True
    if value in ('false', '0', 'f', 'no', 'n'):
        return False
    return None


# ---------- Rotas da API ----------

@app.route('/tasks', methods=['POST'])
def create_task():
    data = get_json_data()

    errors = validate_task_payload(data, partial=False)
    if errors:
        return jsonify({'errors': errors}), 400

    title = data['title'].strip()
    description = data.get('description')

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict()), 201


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task_to_update = Task.query.get_or_404(id)

    data = get_json_data()
    if not data:
        return jsonify({'error': 'Nenhum dado enviado para atualização.'}), 400

    errors = validate_task_payload(data, partial=True)
    if errors:
        return jsonify({'errors': errors}), 400

    if 'title' in data:
        task_to_update.title = data['title'].strip()

    if 'description' in data:
        task_to_update.description = data['description']

    if 'done' in data:
        done_value = data['done']
        if isinstance(done_value, str):
            done_bool = parse_done_value(done_value)
            task_to_update.done = bool(done_bool)
        else:
            task_to_update.done = bool(done_value)

    db.session.commit()
    return jsonify(task_to_update.to_dict())


@app.route('/tasks', methods=['GET'])
def list_tasks():
    """
    Lista tasks com base no filtro abaixo
    - filtro criado para ?done=true/false
    -  as tasks serão ordenadas de forma decrescente por id
    """
    done_param = request.args.get('done')
    query = Task.query

    done_bool = parse_done_value(done_param)
    if done_param is not None and done_bool is None:
        return jsonify({'error': 'Parâmetro done inválido. Use true/false, 1/0.'}), 400

    if done_bool is not None:
        query = query.filter_by(done=done_bool)

    all_tasks = query.order_by(Task.id.desc()).all()
    result = [task.to_dict() for task in all_tasks]
    return jsonify(result)


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    """Retorna uma task pelo id."""
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
