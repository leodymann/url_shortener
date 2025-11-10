# tests/test_main.py

import pytest
from httpx import AsyncClient
from app.main import app
from app.models import URL
from app.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.anyio
async def test_create_url_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"original_url": "https://example.com"}
        response = await ac.post("/urls/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "short_url" in data
        assert data["original_url"] == payload["original_url"]

@pytest.mark.anyio
async def test_get_url_success():
    # Primeiro cria uma URL
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"original_url": "https://example.com/get"}
        create_res = await ac.post("/urls/", json=payload)
        short_url = create_res.json()["short_url"]

        # Agora tenta pegar a URL encurtada
        get_res = await ac.get(f"/urls/{short_url}")
        assert get_res.status_code == 200
        data = get_res.json()
        assert data["original_url"] == payload["original_url"]

@pytest.mark.anyio
async def test_create_url_validation_error():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"original_url": "notaurl"}
        response = await ac.post("/urls/", json=payload)
        assert response.status_code == 422  # Erro de validação do Pydantic

@pytest.mark.anyio
async def test_get_url_not_found():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/urls/nonexistent")
        assert response.status_code == 404
