# Dos formas de ejecutar fastapi
    1. uvicorn main:app
    2. Agregar las lineas de codigo 
        if __name__=="__main__":
            uvicorn.run("main:app",port=8000)
        
        Y luego correr main.py

# Realizar Migraciones

alembic init migrations

# configurar alembic
    - abrir el alembic.ini y modificar la linea de sqlalchemy.url y dejar vacio
# Abrir el env.py de la carpeta migrations
    Copiar esto antes de la funcion run_migrations_offline
    from core.config import settings

    config = context.config
    config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    from app.db.models import Base
    target_metadata = Base.metadata
# Por ultimo ejecutar
alembic revision --autogenerate -m "crear modelos"
alembic upgrade heads

# Desplegar en heroku
Descargar el CLI de heroku
https://devcenter.heroku.com/articles/heroku-cli

    1. heroku login 
    2. heroku git:remote -a URL_PROYECTO
    3. git push heroku master