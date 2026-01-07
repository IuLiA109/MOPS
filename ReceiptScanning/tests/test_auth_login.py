
import pytest
from httpx import AsyncClient

JWT_COOKIE_NAME = "access_token"


@pytest.mark.anyio
async def test_auth_login_using_email_sets_jwt_cookie(async_client: AsyncClient):
    payload = {"email": "a@radush.ro", "password": "Secret123!"}
    r = await async_client.post("/auth/login", json=payload)
    assert r.status_code == 200

    body = r.json()
    assert body["message"] == "Authenticated successfully."

    set_cookie = r.headers.get("set-cookie")
    assert set_cookie is not None, "Expected Set-Cookie header on successful login"
    assert JWT_COOKIE_NAME in set_cookie, f"Expected JWT cookie named '{JWT_COOKIE_NAME}'"


@pytest.mark.anyio
async def test_auth_login_using_username_sets_jwt_cookie(async_client: AsyncClient):
    payload = {"username": "radush", "password": "Secret123!"}
    r = await async_client.post("/auth/login", json=payload)
    assert r.status_code == 200

    set_cookie = r.headers.get("set-cookie")
    assert set_cookie is not None
    assert JWT_COOKIE_NAME in set_cookie


@pytest.mark.anyio
async def test_auth_login_does_not_set_cookie_on_failure(async_client: AsyncClient):
    payload = {"email": "a@radush.ro", "password": "incorrect"}
    r = await async_client.post("/auth/login", json=payload)
    assert r.status_code == 403
    assert r.json()["message"] == "Invalid account details."
    assert r.headers.get("set-cookie") is None


@pytest.mark.anyio
async def test_auth_login_missing_password_returns_422(async_client: AsyncClient):
    payload = {"email": "a@radush.ro"}
    r = await async_client.post("/auth/login", json=payload)
    assert r.status_code == 422


@pytest.mark.anyio
async def test_auth_login_missing_email_and_username_returns_422(async_client: AsyncClient):
    payload = {"password": "Secret123!"}
    r = await async_client.post("/auth/login", json=payload)
    assert r.status_code == 422


@pytest.mark.anyio
async def test_auth_login_with_both_email_and_username_returns_422(async_client: AsyncClient):
    payload = {"email": "a@radush.ro", "username": "radush", "password": "Secret123!"}
    r = await async_client.post("/auth/login", json=payload)
    assert r.status_code == 422
