import bcrypt
from flask import Flask, jsonify, request
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:admin123@127.0.0.1:3306/flask-crud"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

# view login
login_manager.login_view = 'login'

# sessão -> conexão ativa
@login_manager.user_loader
def load_user(user_id):
    print("user id", user_id)
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(str.encode(password), user.password):
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({"message": "Autenticação realizada com sucesso"})
    return jsonify({"message": "Credenciais inválidas"}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso"})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username and password:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso"})

    return jsonify({"message": "Dados inválidos"}), 400

@app.route('/user/<int:user_id>', methods=['GET'])
@login_required
def read_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"username": user.username})
    
    return jsonify({"message": "Usuário não encontrado"}), 404

@app.route('/user', methods=['GET'])
def list_users():
    users = User.query.all()
    list_users = []
    for user in users:
        list_users.append({"username": user.username, "id": user.id})

    return jsonify({"users": list_users})

@app.route('/user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    if user:
        user.password = data.get('password')
        db.session.commit()
        return jsonify({"message": f"Usuário {user_id} atualizado com sucesso"})
    
    return jsonify({"message": "Usuário não encontrado"}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)

    if  user_id == current_user.id:
        return jsonify({"message": "Remoção não permitida"}), 403

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"Usuário {user_id} removido com sucesso"})
    
    return jsonify({"message": "Usuário não encontrado"}), 404

# Iniclialização manual, ambiente dev
if __name__ == "__main__":
    app.run(debug=True)