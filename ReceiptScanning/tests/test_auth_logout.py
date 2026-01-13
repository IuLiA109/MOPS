import pytest
from httpx import AsyncClient

JWT_COOKIE_NAME = "access_token"


@pytest.mark.anyio
async def test_auth_logout_clears_cookie(async_client: AsyncClient):
    payload = {"username": "radush", "email": "a@radush.ro", "password": "Secret123!"}

    r1 = await async_client.post("/auth/register", json=payload)
    assert r1.status_code == 201,r1.json()

    r = await async_client.post("/auth/login", json={"email": "a@radush.ro", "password": "Secret123!"})
    assert r.status_code == 200

    out = await async_client.post("/auth/logout")
    assert out.status_code in (200, 204)

    set_cookie = out.headers.get("set-cookie")
    assert set_cookie is not None
    assert JWT_COOKIE_NAME in set_cookie
    assert ("Max-Age=0" in set_cookie) or ("expires=" in set_cookie.lower())
