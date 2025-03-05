import pytest
from fastapi.testclient import TestClient
from app.main import app  

client = TestClient(app)

@pytest.fixture
def new_user():
    return {
        "email": "testuser77@example.com",
        "password": "securepassword"
    }

@pytest.fixture
def access_token(new_user):
    client.post("/auth/register", json=new_user)  

    login_data = {
        "username": new_user["email"],
        "password": new_user["password"]
    }
    response = client.post("/auth/login", data=login_data)
    
    assert response.status_code == 200 
    token = response.json().get("access_token")
    assert token is not None  
    return token 

@pytest.fixture
def auth_headers(access_token):
    return {"Authorization": f"Bearer {access_token}"}

def test_register_user(new_user):
    response = client.post("/auth/register", json=new_user)
    assert response.status_code == 201
    assert response.json() == {"msg": "success"}

def test_login_user(new_user):
    client.post("/auth/register", json=new_user)

    login_data = {
        "username": new_user["email"],
        "password": new_user["password"]
    }
    
    response = client.post("/auth/login", data=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_all_servers_health_status(auth_headers):
    response = client.get("/health/all", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)  

def test_register_server(auth_headers):
    server_data = {
        "server_name": "Test Server",
    }

    response = client.post("/servers/", json=server_data, headers=auth_headers)
    assert response.status_code == 201  
    
    server_id = response.json()  
    print(f"Server ID: {server_id}")
    return server_id

def test_get_server_health_status(auth_headers):
    server_id = test_register_server(auth_headers)
    
    response = client.get(f"/health/{server_id}", headers=auth_headers)
    
    assert response.status_code == 200

def test_sensor_register(auth_headers):
    server_id = test_register_server(auth_headers)
    sensor_data = {
        "server_ulid": server_id,  
        "timestamp": "2025-03-05T12:00:00Z",
        "temperature": 22.5,
        "humidity": 60.0
    }

    response = client.post("/data/", json=sensor_data, headers=auth_headers)
    assert response.status_code == 201  
    assert response.json() == {'msg': 'success'}


def test_sensor_data_aggregation(auth_headers):
    server_id = test_register_server(auth_headers)
    params = {
        "server_ulid": server_id,  
        "start_time": "2025-03-01T00:00:00Z",
        "end_time": "2025-03-05T23:59:59Z",
        "sensor_type": "temperature",
        "aggregation": "hour"
    }

    response = client.get("/data/", params=params, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)  
    assert "timestamp" in data[0] 
    assert "temperature" in data[0]  

