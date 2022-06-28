import hashlib  # importa la libreria hashlib 
import sqlite3 
import os 
from typing import List 
from fastapi import Depends, FastAPI, HTTPException, status 
from fastapi.security import HTTPBasic, HTTPBasicCredentials 
from pydantic import BaseModel 
from typing import Union  

app = FastAPI() 

DATABASE_URL = os.path.join("sql/clientes.sqlite") 

security = HTTPBasic() 

class Usuarios(BaseModel): 
    username: str 
    level: int 

class Respuesta (BaseModel) :  
    message: str  
           
class Cliente (BaseModel):  
    id_cliente: int  
    nombre: str  
    email: str  


@app.get("/", response_model=Respuesta) 
async def index(): 
    return {"message": "API REST"} 


def get_current_level(credentials: HTTPBasicCredentials = Depends(security)):
    password_b = hashlib.md5(credentials.password.encode())
    password = password_b.hexdigest()
    with sqlite3.connect(DATABASE_URL) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT level FROM usuarios WHERE username = ? and password = ?",
            (credentials.username, password),)
        user = cursor.fetchone()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
    return user[0] #ADMIN

@app.get("/clientes/", response_model=List[Cliente],status_code=status.HTTP_202_ACCEPTED,
summary="Regresa una lista de usuarios",description="Regresa una lista de usuarios")
async def clientes(level: int = Depends(get_current_level)):
    if level == 1: 
        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM clientes')
            response = cursor.fetchall()
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post("/clientes/", response_model=Respuesta,status_code=status.HTTP_202_ACCEPTED,
summary="Inserta un usuario",description="Inserta un usuario")
async def clientes(level: int = Depends(get_current_level),nombre: str="", email:str=""):
    if level == 0: 
        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("INSERT INTO clientes (nombre, email) VALUES (? , ?);",(nombre, email))
            connection.commit()
            response = {"message":"Cliente agregado"}
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.put("/clientes/", response_model=List[Cliente],status_code=status.HTTP_202_ACCEPTED,
summary="Actualiza un usuario",description="Actualiza un usuario")
async def clientes(level: int = Depends(get_current_level), id_cliente: int=0, nombre: str="", email:str=""):
    if level == 0: 
        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("UPDATE clientes SET nombre =?, email= ? WHERE id_cliente =?;",(nombre, email, id_cliente))
            connection.commit()
            response = {"message":"Cliente actualizado"}
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.delete("/clientes/", response_model=List[Cliente],status_code=status.HTTP_202_ACCEPTED,
summary="Elimina un usuario",description="Elimina un usuario")
async def clientes(level: int = Depends(get_current_level), id_cliente: int=0, nombre: str="", email:str=""):
    if level == 0: 
        with sqlite3.connect(DATABASE_URL) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente= '{id_cliente}';".format(id_cliente=id_cliente))
            connection.commit()
            response = {"message":"Cliente eliminado"}
            return response
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Don't have permission to access this resource",
            headers={"WWW-Authenticate": "Basic"},
        )


















        import hashlib  # importa la libreria hashlib 
import sqlite3 
import os 
from typing import List 
from fastapi import Depends, FastAPI, HTTPException, status 
from fastapi.security import HTTPBasic, HTTPBasicCredentials 
from pydantic import BaseModel 
from typing import Union  

app = FastAPI() 

DATABASE_URL = os.path.join("sql/clientes.sqlite") 

security = HTTPBasic() 

class Usuarios(BaseModel): 
    username: str 
    level: int 

class Respuesta (BaseModel) :  
     message: str  
           
class Cliente (BaseModel):  
     id_cliente: int  
     nombre: str  
     email: str  
   
class ClienteIN(BaseModel): 
    nombre: str 
    email : str 

@app.get("/", response_model=Respuesta) 
async def index(): 
    return {"message": "API REST"} 
  
@app.get("/clientes/") 
async def clientes(): 
     with sqlite3.connect('sql/clientes.sqlite') as connection: 
         connection.row_factory = sqlite3.Row 
         cursor=connection.cursor() 
         cursor.execute("SELECT * FROM clientes") 
         response=cursor.fetchall() 
         return response 
         return {"message": "API REST"} 
  
@app.get("/clientes/{id}") 
async def clientes(id): 
     with sqlite3.connect('sql/clientes.sqlite') as connection: 
         connection.row_factory = sqlite3.Row 
         cursor=connection.cursor() 
         cursor.execute("SELECT * FROM clientes WHERE id_cliente={}".format(int(id))) 
         response=cursor.fetchall() 
         return response

@app.post("/clientes/", response_model=Respuesta)
def post_cliente(cliente: ClienteIN):
    with sqlite3.connect('sql/clientes.sqlite') as connection:
        connection.row_factory = sqlite3.Row
        cursor=connection.cursor()
        cursor.execute("INSERT INTO clientes(nombre,email) VALUES(?,?)", (cliente.nombre,cliente.email))
        cursor.fetchall()
        response = {"message":"Cliente insertado"}
        return response



@app.put("/clientes/", response_model=Respuesta)
async def clientes_update(nombre: str="", email:str="", id_cliente:int=0):
    with sqlite3.connect("sql/clientes.sqlite") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("UPDATE clientes SET nombre =?, email= ? WHERE id_cliente =?;",(nombre, email, id_cliente))
        cursor.fetchall()
        response = {"message":"Cliente actualizado"}
        return response

@app.delete("/clientes/{id}") 
async def clientes(id): 
     with sqlite3.connect('sql/clientes.sqlite') as connection: 
         connection.row_factory = sqlite3.Row 
         cursor=connection.cursor() 
         cursor.execute("DELETE FROM clientes WHERE id_cliente={}".format(int(id))) 
         cursor.fetchall() 
         response = {"message":"Cliente eliminado"}
         return response


 
def get_current_level(credentials: HTTPBasicCredentials = Depends(security)): 
    password_b = hashlib.md5(credentials.password.encode())  
    password = password_b.hexdigest() 
    with sqlite3.connect(DATABASE_URL) as connection: 
        cursor = connection.cursor() 
        cursor.execute( 
            "SELECT level FROM usuarios WHERE username = ? and password = ?", 
            (credentials.username, password), 
        ) 
        user = cursor.fetchone()  
        if not user: 
            raise HTTPException(  
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password", 
                headers={"WWW-Authenticate": "Basic"}, 
            ) 
    return user[1] 
@app.get( 
    "/clientes/", 
    response_model=List[Usuarios], 
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Regresa una lista de clientes", 
    description="Regresa una lista de clientes", 
) 
async def get_clientes(level: int = Depends(get_current_level)): 
    if level == 1:  # usuario 
        with sqlite3.connect(DATABASE_URL) as connection: 
            connection.row_factory = sqlite3.Row 
            cursor = connection.cursor() 
            cursor.execute("SELECT username, level FROM usuarios") 
            clientes = cursor.fetchall() 
            return clientes 
    else: 
        raise HTTPException( 
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Don't have permission to access this resource", 
            headers={"WWW-Authenticate": "Basic"}, 
        )

def getid_current_level(id:int=0,credentials: HTTPBasicCredentials = Depends(security)): 
    password_b = hashlib.md5(credentials.password.encode())  
    password = password_b.hexdigest() 
    with sqlite3.connect(DATABASE_URL) as connection: 
        cursor = connection.cursor() 
        cursor.execute( 
            "SELECT level FROM usuarios WHERE username = ? and password = ?", 
            (credentials.username, password), 
            "SELECT * FROM clientes WERE WHERE id_cliente =?" (id),
        ) 
        user = cursor.fetchone()  
        if not user: 
            raise HTTPException(  
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password", 
                headers={"WWW-Authenticate": "Basic"}, 
            ) 
    return user[1] 
@app.get( 
    "/clientes/{id}", 
    response_model=List[Usuarios], 
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Regresa una lista de un cliente", 
    description="Regresa una lista de un cliente", 
) 
async def get_clientes(level: int = Depends(getid_current_level)): 
    if level == 1:  # usuario 
        with sqlite3.connect(DATABASE_URL) as connection: 
            connection.row_factory = sqlite3.Row 
            cursor = connection.cursor() 
            cursor.execute("SELECT username, level FROM usuarios") 
            clientes = cursor.fetchall() 
            return clientes 
    else: 
        raise HTTPException( 
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Don't have permission to access this resource", 
            headers={"WWW-Authenticate": "Basic"}, 
        )


 
def post_current_level(cliente: ClienteIN, credentials: HTTPBasicCredentials = Depends(security)): 
    password_b = hashlib.md5(credentials.password.encode())  
    password = password_b.hexdigest() 
    with sqlite3.connect(DATABASE_URL) as connection: 
        cursor = connection.cursor() 
        cursor.execute( 
            "SELECT level FROM usuarios WHERE username = ? and password = ?", 
            (credentials.username, password), 
            "INSERT INTO clientes(nombre,email) VALUES(?,?)", (cliente.nombre,cliente.email)
        ) 
        user = cursor.fetchone()  
        if not user: 
            raise HTTPException(  
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password", 
                headers={"WWW-Authenticate": "Basic"}, 
            ) 
    return user[0] 
@app.post( 
    "/clientes/", 
    response_model=Respuesta, 
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Inserta Clientes", 
    description="Inserta Clientes", 
    
)       
    
async def post_clientes(level: int = Depends(post_current_level)): 
    if level == 0:  # usuario 
        with sqlite3.connect(DATABASE_URL) as connection: 
            connection.row_factory = sqlite3.Row 
            cursor = connection.cursor() 
            cursor.execute("SELECT username, level FROM usuarios") 
            clientes = cursor.fetchall() 
            return clientes 
    else: 
        raise HTTPException( 
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Don't have permission to access this resource", 
            headers={"WWW-Authenticate": "Basic"}, 
        )


def put_current_level(nombre: str="", email:str="", id_cliente:int=0, credentials: HTTPBasicCredentials = Depends(security)): 
    password_b = hashlib.md5(credentials.password.encode())  
    password = password_b.hexdigest() 
    with sqlite3.connect(DATABASE_URL) as connection: 
        cursor = connection.cursor() 
        cursor.execute( 
            "SELECT level FROM usuarios WHERE username = ? and password = ?", 
            (credentials.username, password), 
            "INSERT INTO clientes(nombre,email) VALUES(?,?)", (cliente.nombre,cliente.email)
        ) 
        user = cursor.fetchone()  
        if not user: 
            raise HTTPException(  
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password", 
                headers={"WWW-Authenticate": "Basic"}, 
            ) 
    return user[0] 
@app.put( 
    "/clientes/", 
    response_model=Respuesta, 
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Actualiza Clientes", 
    description="Actualiza Clientes", 
    
)       
    
async def put_clientes(level: int = Depends(put_current_level)): 
    if level == 0:  # usuario 
        with sqlite3.connect(DATABASE_URL) as connection: 
            connection.row_factory = sqlite3.Row 
            cursor = connection.cursor() 
            cursor.execute("UPDATE clientes SET nombre =?, email= ? WHERE id_cliente =?;",(nombre, email, id_cliente)) 
            clientes = cursor.fetchall() 
            return clientes 
    else: 
        raise HTTPException( 
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Don't have permission to access this resource", 
            headers={"WWW-Authenticate": "Basic"}, 
        )

       
def delete_current_level(id: int=0, credentials: HTTPBasicCredentials = Depends(security)): 
    password_b = hashlib.md5(credentials.password.encode())  
    password = password_b.hexdigest() 
    with sqlite3.connect(DATABASE_URL) as connection: 
        cursor = connection.cursor() 
        cursor.execute( 
            "SELECT level FROM usuarios WHERE username = ? and password = ?", 
            (credentials.username, password), 
            "DELETE FROM clientes WHERE id_cliente=?;",(id)
        ) 
        user = cursor.fetchone()  
        if not user: 
            raise HTTPException(  
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password", 
                headers={"WWW-Authenticate": "Basic"}, 
            ) 
    return user[0] 
@app.delete( 
    "/clientes/{id}", 
    response_model=Respuesta, 
    status_code=status.HTTP_202_ACCEPTED, 
    summary="Elimina Clientes", 
    description="Elimina Clientes", 
) 
async def delete_clientes(level: int = Depends(delete_current_level)): 
    if level == 0:  # usuario 
        with sqlite3.connect(DATABASE_URL) as connection: 
            connection.row_factory = sqlite3.Row 
            cursor = connection.cursor() 
            cursor.execute("SELECT username, level FROM usuarios") 
            clientes = cursor.fetchall() 
            return clientes 
    else: 
        raise HTTPException( 
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Don't have permission to access this resource", 
            headers={"WWW-Authenticate": "Basic"}, 
        )