def test_full_pipeline(client):
    with open("tests/assets/sample.mp4", "rb") as f:
        response = client.post(
            "/api/v2/analyze",
            files={"file": ("sample.mp4", f, "video/mp4")}
        )

    assert response.status_code == 200

    data = response.json()

    assert "overall_score" in data
    assert "artifacts" in data
    assert "annotated_video_url" in data["artifacts"]