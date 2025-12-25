def test_initial_value_is_zero(client):
    response = client.get("/api/counter")
    assert response.status_code == 200
    assert response.json["value"] == 0


def test_increment_increases_value(client):
    response = client.post("/api/counter/increment")
    assert response.status_code == 200
    assert response.json["value"] == 1

    response = client.get("/api/counter")
    assert response.json["value"] == 1


def test_counter_cannot_be_negative(client):
    for _ in range(5):
        response = client.post("/api/counter/decrement")
        assert response.status_code == 400

    response = client.get("/api/counter")
    assert response.json["value"] == 0


def test_double_increment(client):
    response = client.post("/api/counter/increment")
    assert response.json["value"] == 1

    response = client.post("/api/counter/increment")
    assert response.json["value"] == 2


def test_any_route(client):
    response = client.get("/api/counter/blah-blah-blah")
    assert response.status_code == 200