import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_register_creates_user(async_client: AsyncClient):
    payload = {"username": "radush", "email": "a@radush.ro", "password": "Secret123!"}
    r = await async_client.post("/auth/register", json=payload)
    assert r.status_code == 201

    body = r.json()
    assert "email" not in body
    assert "password" not in body
    assert "token" not in body
    assert body["message"] == "Registered successfully."


@pytest.mark.anyio
async def test_register_duplicate_email(async_client: AsyncClient):
    payload = {"username": "radush", "email": "a@radush.ro", "password": "Secret123!"}

    r1 = await async_client.post("/auth/register", json=payload)
    assert r1.status_code == 201

    payload["username"] = "radush02"
    r2 = await async_client.post("/auth/register", json=payload)
    assert r2.status_code == 409
    assert r2.json()["message"] == "Email already in use."


@pytest.mark.anyio
async def test_register_duplicate_username(async_client: AsyncClient):
    payload = {"username": "radush", "email": "a@radush.ro", "password": "Secret123!"}

    r1 = await async_client.post("/auth/register", json=payload)
    assert r1.status_code == 201

    payload["email"] = "another@radush.ro"
    r2 = await async_client.post("/auth/register", json=payload)
    assert r2.status_code == 409
    assert r2.json()["message"] == "Username already taken."


@pytest.mark.anyio
async def test_register_insecure_password(async_client: AsyncClient):
    payload = {"username": "radush", "email": "a@radush.ro", "password": "pass"}
    r = await async_client.post("/auth/register", json=payload)
    assert r.status_code == 403
    assert (
        r.json()["message"]
        == "Password must contain at least 8 characters, one uppercase character, one lowercase character, one number, and one special character."
    )


@pytest.mark.anyio
async def test_register_missing_fields_returns_422(async_client: AsyncClient):
    r = await async_client.post("/auth/register", json={"username": "radush"})
    assert r.status_code == 422


@pytest.mark.anyio
async def test_register_invalid_email_returns_422(async_client: AsyncClient):
    payload = {"username": "radush", "email": "not-an-email", "password": "Secret123!"}
    r = await async_client.post("/auth/register", json=payload)
    assert r.status_code == 422
