from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_invalid_provider():
    resp = client.post(
        "/llm/complete",
        json={
            "provider": "unknown",
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "Hello"}],
        },
    )
    assert resp.status_code == 400

