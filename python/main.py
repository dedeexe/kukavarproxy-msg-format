from kukavarproxy import *
from fastapi import FastAPI, HTTPException
import time


#robot = KUKA('172.31.1.147', 7000)

#robot.write("$OV_PRO",33)
#print (robot.read("$OV_PRO"))

robot = None
MAX_ID = 76
MIN_ID = 1

def start_connection():
    global robot
    robot = KUKA('127.0.0.1', 7001)


def check_item(id: int):
    global MAX_ID, MIN_ID
    if id < MIN_ID or id > MAX_ID:
        print(f"ID WRONG {id}")
        raise HTTPException(status_code=404, detail=f"Item not found. Select an id from {MIN_ID} to {MAX_ID}")

def handle_item(id: int, operation: int): 
    global robot
    check_item(id)

    try:
        start_connection()
        robot.write("operacao", operation)
        operation = robot.read("operacao")
        robot.write("numero", id)
        number = robot.read("numero")
        return {"operacao": operation, "numero": number}
    except SystemError as error:
        raise HTTPException(status_code=500, detail=error)

def get_item(id: int): 
    """
    Função para tirar item da estante
    Cheque se o valor da operação é este mesmo, acredito que seja:
    - 1 para colocar na estante
    - 2 para guardar na estante
    """
    handle_item(id, 2)

def store_item(id: int): 
    """
    Função para guarda item da estante
    Cheque se o valor da operação é este mesmo, acredito que seja:
    - 1 para colocar na estante
    - 2 para guardar na estante
    """
    handle_item(id, 1)

#
# API
#
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "It works"}

#Gets a shoe from the drawer
@app.get("/get/item/{item_id}")
async def get_item(item_id: int):
    result = get_item(item_id)
    return result

#Stores a shoe into drawer
@app.get("/store/item/{item_id}")
async def store_item(item_id: int):
    result = store_item(item_id)
    return result


#
# Inicia o serviço - Apenas imprime mensagem informanto que deu tudo certo
#

print("Servidor iniciado com sucesso.")
