from flask import Flask, request, jsonify, render_template
import sqlite3, bcrypt, re
from datetime import datetime

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
   db = sqlite3.connect(DATABASE)
   db.row_factory = sqlite3.Row
   return db

def init_db():
   with app.app_context():
       db = get_db()
       with app.open_resource('schema.sql', mode='r') as f:
           db.cursor().executescript(f.read())
           db.commit() # Salva as mudanças

def is_valid_email(email):
   return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def get_current_time():
   return datetime.now().isoformat()

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/initdb')
def initialize_database():
   init_db()
   return 'Banco de dados inicializado'

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        login = request.json.get('login')
        senha = request.json.get('senha')
        nome = request.json.get('nome')

        if not login or not senha or not nome:
            return jsonify({'error': 'Login, senha e nome são obrigatórios'}), 400

        if not is_valid_email(login):
            return jsonify({'error': 'Login deve ser um e-mail válido'}), 400

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE login = ?', (login,))
            if cursor.fetchone():
                return jsonify({'error': 'Login já existe'}), 400

            # criptografa a senha
            hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            created_at = get_current_time()
            cursor.execute('INSERT INTO usuarios (login, senha, nome, created) VALUES (?, ?, ?, ?)',
                           (login, hashed_senha, nome, created_at))
            db.commit()
            return jsonify({'message': 'Usuário cadastrado com sucesso!'}), 201
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login_usuario():
    if request.method == 'POST':
        login = request.json.get('login')
        senha = request.json.get('senha')

        if not login or not senha:
            return jsonify({'error': 'Login e senha são obrigatórios'}), 400

        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE login = ?', (login,))
            usuario = cursor.fetchone()

            if usuario: # verifica se o usuário está ativo e se a senha funciona
                if usuario['status'] == 0:
                    return jsonify({'error': 'Usuário bloqueado, não é possível fazer login'}), 403

                if bcrypt.checkpw(senha.encode('utf-8'), usuario['senha']):
                    return jsonify({'redirect': 'https://www.catolicasc.org.br'}), 200

            return jsonify({'error': 'Login ou senha inválidos'}), 401
        except sqlite3.Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            db.close()

    return render_template('login.html')

@app.route('/alteracao')
def alteracao():
   return render_template('alteracao.html')

@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
   try:
       db = get_db()
       cursor = db.cursor()
       cursor.execute('SELECT id, login, nome, status FROM usuarios WHERE id = ?', (usuario_id,))
       usuario = cursor.fetchone()

       if usuario:
           return jsonify({
               'id': usuario['id'],
               'login': usuario['login'],
               'nome': usuario['nome'],
               'status': usuario['status']
           }), 200
       else:
           return jsonify({'error': 'Usuário não encontrado'}), 404
   except sqlite3.Error as e:
       return jsonify({'error': str(e)}), 500
   finally:
       db.close()

@app.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
   novo_login = request.json.get('login')
   senha = request.json.get('senha')
   nome = request.json.get('nome')
   status = request.json.get('status')

   try:
       db = get_db()
       cursor = db.cursor()
       cursor.execute('SELECT * FROM usuarios WHERE id = ?', (usuario_id,))
       usuario = cursor.fetchone()

       if not usuario:
           return jsonify({'error': 'Usuário não encontrado'}), 404

       if novo_login and novo_login != usuario['login']:
           cursor.execute('SELECT * FROM usuarios WHERE login = ? AND id != ?', (novo_login, usuario_id))
           if cursor.fetchone():
               return jsonify({'error': 'Login já existe'}), 400

       if senha:
           hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
           cursor.execute('UPDATE usuarios SET login = ?, senha = ?, nome = ?, status = ?, modified = ? WHERE id = ?',
                          (novo_login if novo_login else usuario['login'], hashed_senha, nome if nome else usuario['nome'], status if status else usuario['status'], get_current_time(), usuario_id))
       else:
           cursor.execute('UPDATE usuarios SET login = ?, nome = ?, status = ?, modified = ? WHERE id = ?',
                          (novo_login if novo_login else usuario['login'], nome if nome else usuario['nome'], status if status else usuario['status'], get_current_time(), usuario_id))

       db.commit()
       return jsonify({'message': 'Usuário atualizado com sucesso!'})
   except sqlite3.Error as e:
       return jsonify({'error': str(e)}), 500
   finally:
       db.close()

@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
   try:
       db = get_db()
       cursor = db.cursor()
       cursor.execute('UPDATE usuarios SET status = 0 WHERE id = ?', (usuario_id,))
       db.commit()
       return jsonify({'message': 'Usuário bloqueado com sucesso'})
   except sqlite3.Error as e:
       return jsonify({'error': str(e)}), 500
   finally:
       db.close()

if __name__ == '__main__':
   app.run(debug=True)