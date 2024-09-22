import pytest
from app.core.config import Settings

def test_access_token_expire_minutes_is_int():
    settings = Settings()
    numero = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    assert isinstance(numero, int), "A variável não é um inteiro"
