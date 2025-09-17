from config_db import app
from routes.auth import auth_route
from routes.home import home_route

# Registra os blueprints
app.register_blueprint(auth_route)
app.register_blueprint(home_route)

if __name__ == '__main__':
    # Garante que as tabelas são criadas
    from config_db import db
    with app.app_context():
        db.create_all()
    app.run(debug=True)
