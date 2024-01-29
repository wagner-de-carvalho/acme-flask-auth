# acme-flask-auth
API de autenticação com banco de dados

### Criar banco de dados via flask shell com Flask Alchemy
1 - `flask shell` = abre o shell do flask
2 - `db.create_all()` = cria o banco de dados
3 - `db.session` = objeto de sessão do banco de dados
4 - `db.session.commit()` = executa as operações no banco de dados

### Criar objeto com SQLAlchemy
1 - `user = User(username="admin", password="123")`
2 - `db.session.add(user)`
3 - `db.session.commit()`

