import pytest
from httpx import AsyncClient

JWT_COOKIE_NAME = "access_token"


async def _login(async_client: AsyncClient):
    payload = {"username":"radush","email": "a@radush.ro", "password": "Secret123!"}
    r = await async_client.post("/auth/register", json=payload)
    assert r.status_code == 201
    payload = {"email": "a@radush.ro", "password": "Secret123!"}
    r = await async_client.post("/auth/login", json=payload)
    print(r.json())
    assert r.status_code == 200
    return r


@pytest.mark.anyio
async def test_auth_me_requires_auth(async_client: AsyncClient):
    r = await async_client.get("/auth/me")
    assert r.status_code in (401, 403)


@pytest.mark.anyio
async def test_auth_me_returns_current_user(async_client: AsyncClient):
    login_r = await _login(async_client)
    cookie_value = login_r.cookies.get(JWT_COOKIE_NAME)
    assert cookie_value is not None, f"Missing '{JWT_COOKIE_NAME}' cookie after login"

    async_client.cookies.set(JWT_COOKIE_NAME, cookie_value)

    r = await async_client.get("/auth/me")
    assert r.status_code == 200
    body = r.json()
    assert "password" not in body
    assert "token" not in body


@pytest.mark.anyio
async def test_auth_me_rejects_invalid_cookie(async_client: AsyncClient):
    async_client.cookies.set(JWT_COOKIE_NAME, "doesnt.exist")
    r = await async_client.get("/auth/me")
    assert r.status_code in (401, 403)
