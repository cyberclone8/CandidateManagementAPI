import pytest

@pytest.mark.asyncio
async def test_candidate_application_flow(client):
    login = await client.post("/auth/login", data={"username": "admin@example.com", "password": "admin"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    candidate = await client.post("/candidates", json={
        "full_name": "Jane Doe",
        "email": "jane@example.com",
        "skills": ["SQL"]
    }, headers=headers)

    cid = candidate.json()["id"]

    apply = await client.post(f"/candidates/{cid}/applications", json={"job_title": "Backend Dev"}, headers=headers)
    assert apply.status_code == 200
    app_id = apply.json()["id"]

    patch = await client.patch(f"/applications/{app_id}", json={"status": "HIRED"}, headers=headers)
    assert patch.status_code == 200
    assert patch.json()["status"] == "HIRED"