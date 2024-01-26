from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)

@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello'

# Iniclialização manual, ambiente dev
if __name__ == "__main__":
    app.run(debug=True)