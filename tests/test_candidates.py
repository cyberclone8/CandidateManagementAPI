import pytest

@pytest.mark.asyncio
async def test_create_and_get_candidate(client):
    login = await client.post("/auth/login", data={"username": "admin@example.com", "password": "admin"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "full_name": "John Doe",
        "email": "john@example.com",
        "skills": ["Python", "FastAPI"]
    }
    create = await client.post("/candidates", json=payload, headers=headers)
    assert create.status_code == 200

    candidate_id = create.json()["id"]
    detail = await client.get(f"/candidates/{candidate_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["full_name"] == "John Doe"