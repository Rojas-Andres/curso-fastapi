# Dos formas de ejecutar fastapi
    1. uvicorn main:app
    2. Agregar las lineas de codigo 
        if __name__=="__main__":
            uvicorn.run("main:app",port=8000)
        
        Y luego correr main.py