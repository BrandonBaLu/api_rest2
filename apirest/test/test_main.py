from fastapi.testclient import TestClient

from code.main import  app

clientes = TestClient(app)


def test_index():
    response= clientes.get("/") #request
    data = {"message": "API REST"}
    assert response.status_code == 200
    assert response.json() == data



def test_clientes():
    response = clientes.get("/clientes/") #request,
    data = [{"id_cliente":1,"nombre":"Brandon","email":"patolucas.bbl@gmail.com"},
    {"id_cliente":2,"nombre":"Erick","email":"Erickbabytaz@gmail.com"},
    {"id_cliente":3,"nombre":"Toño","email":"TonyBalde@gmail.com"}]
    assert response.status_code == 200
    assert response.json() == data

def test_clientes():
    response = clientes.get("/clientes/1") #request
    data = [{"id_cliente":1,"nombre":"Brandon","email":"patolucas.bbl@gmail.com"}]
    assert response.status_code == 200
    assert response.json() == data