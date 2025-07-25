import pytest

@pytest.mark.asyncio
async def test_login(client):
    response = await client.post("/auth/login", data={"username": "admin@example.com", "password": "admin"})
    assert response.status_code == 200
    assert "access_token" in response.json()