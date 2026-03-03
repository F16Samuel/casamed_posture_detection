import io


def test_health_endpoint(client):
    response = client.get("/api/v2/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_invalid_file_format(client):
    fake_file = io.BytesIO(b"not a video")

    response = client.post(
        "/api/v2/analyze",
        files={"file": ("test.txt", fake_file, "text/plain")}
    )

    assert response.status_code == 400