from werkzeug.exceptions import HTTPException
from app.routes.planet_routes import validate_model
from app.models.planet import Planet
import pytest

#### POST ####
def test_create_planet_valid_request(client):
    # Act
    response = client.post("/planets", json = {
        "description": "Mars is a dusty, cold, desert world with a very thin atmosphere.",
        "length_of_year": 687,
        "name": "Mars"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Planet Mars successfully created"

def test_create_planet_invalid_request_empty_name(client):
    # Act
    response = client.post("/planets", json = {
        "name": "", 
        "description": "This unknown planet is the imaginary planet for purpose of testing.", 
        "length_of_year": 10})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == "Invalid request"

def test_create_planet_invalid_request_lenght_of_year_zero(client):
    # Act
    response = client.post("/planets", json = {
        "name": "Test", 
        "description": "This unknown planet is the imaginary planet for purpose of testing.", 
        "length_of_year": 0})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == "Invalid request"

def test_create_planet_invalid_request_lenght_of_year_negative(client):
    # Act
    response = client.post("/planets", json = {
        'name': 'Test', 
        'description': 'This unknown planet is the imaginary planet for purpose of testing.', 
        'length_of_year': -100})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == "Invalid request"

def test_create_planet_invalid_request_description_empty(client):
    # Act
    response = client.post("/planets", json = {
        'name': 'Test', 
        'description': '', 
        'length_of_year': 10})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == "Invalid request"

#### PUT ####
def test_update_planet_valid_request(client, one_planet):
    # Act
    planet_id = one_planet.id
    response = client.put(f"/planets/{one_planet.id}", json = {
        "description": "Mercury is the smallest planet in the Solar System and the closest to the Sun.",
        "length_of_year": 88,
        "name": "Mercury_updated"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == f"Planet {planet_id} successfully updated"

def test_update_planet_not_exist_id(client, one_planet):
    # Act
    response = client.put("/planets/9", json = {
        "description": "Mars is a dusty, cold, desert world with a very thin atmosphere.",
        "length_of_year": 687,
        "name": "Mars"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == f"Planet 9 not found"

def test_update_planet_invalid_type_id(client, one_planet):
    # Act
    planet_id = "hello"
    response = client.put(f"/planets/{planet_id}", json = {
        "description": "Mars is a dusty, cold, desert world with a very thin atmosphere.",
        "length_of_year": 687,
        "name": "Mars"
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == f"Planet {planet_id} invalid"

def test_update_planet_invalid_request_empty_name(client, one_planet):
    # Act
    response = client.put(f"/planets/{one_planet.id}", json = {
        "name": "", 
        "description": "This unknown planet is the imaginary planet for purpose of testing.", 
        "length_of_year": 10})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == "Invalid request"

def test_update_planet_invalid_request_lenght_of_year_zero(client, one_planet):
    # Act
    response = client.put(f"/planets/{one_planet.id}", json = {
        "name": "Test", 
        "description": "This unknown planet is the imaginary planet for purpose of testing.", 
        "length_of_year": 0})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == "Invalid request"

def test_update_planet_invalid_request_lenght_of_year_negative(client, one_planet):
    # Act
    response = client.put(f"/planets/{one_planet.id}", json = {
        'name': 'Test', 
        'description': 'This unknown planet is the imaginary planet for purpose of testing.', 
        'length_of_year': -100})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == "Invalid request"

def test_update_planet_invalid_request_description_empty(client, one_planet):
    # Act
    response = client.put(f"/planets/{one_planet.id}", json = {
        'name': 'Test', 
        'description': '', 
        'length_of_year': 10})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == "Invalid request"

#### DELETE ####
def test_delete_planet_by_id_valid_request_with_zero_moons(client, one_planet):
    # Act
    planet_id = one_planet.id
    response = client.delete(f"/planets/{planet_id}")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == f"Planet {planet_id} successfully deleted"

def test_delete_planet_by_id_valid_request_with_two_moons(client, one_planet_with_moons):
    # Act
    planet_id = one_planet_with_moons.id
    response = client.delete(f"/planets/{planet_id}")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == f"Planet {planet_id} successfully deleted"

def test_delete_planet_by_id_invalid_id(client, one_planet):
    # Act
    planet_id = "hello"
    response = client.delete(f"/planets/{planet_id}")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == f"Planet {planet_id} invalid"

def test_delete_planet_by_not_existed_id(client, one_planet):
    planet_id = 9
    response = client.delete(f"/planets/{planet_id}")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 404
    assert response_body == f"Planet {planet_id} not found"
    
####GET####   
def test_get_planet1_from_fixture_one_planet_return_200(client,one_planet):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id":1,
        "name": "Mercury",
        "length_of_year": 88,
        "description": "Mercury is the smallest planet in the Solar System and the closest to the Sun.",
        "moons": []
    }

def test_get_planet1_from_fixture_three_planet_return_200(client,three_planets):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id":1,
        "name": "Mercury",
        "length_of_year": 88,
        "description": "Mercury is the smallest planet in the Solar System and the closest to the Sun.",
        "moons": []
    }

def test_get_planet1_no_fixture_return_404(client):
    # Act
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == "Planet 1 not found"

def test_get_planets_in_array_return_200(client,one_planet):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
        "id":1,
        "name": "Mercury",
        "length_of_year": 88,
        "description": "Mercury is the smallest planet in the Solar System and the closest to the Sun.",
        "moons": []
    }
    ]

def test_get_planets_in_array_with_fixture_three_planets_return_200(client,three_planets):
    # Act
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
        "id":1,
        "name": "Mercury",
        "length_of_year": 88,
        "description": "Mercury is the smallest planet in the Solar System and the closest to the Sun.",
        "moons": []
    },
    {
        "id":2,
        "name": "Venus",
        "length_of_year": 225,
        "description": "Venus spins slowly in the opposite direction from most planets.",
        "moons": []
    },
    {
        "id":3,
        "name": "Earth",
        "length_of_year": 365,
        "description": "Earth — our home planet.",
        "moons": []
    }
]

