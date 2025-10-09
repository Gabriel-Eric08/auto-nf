from config_db import app

print("Conectando com URI:", app.config["SQLALCHEMY_DATABASE_URI"])