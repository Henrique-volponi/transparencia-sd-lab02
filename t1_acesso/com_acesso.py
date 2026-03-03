import json
import os
import requests
from abc import ABC, abstractmethod

class ConfigRepository(ABC):
    @abstractmethod
    def get(self, key: str) -> dict:
        pass

class LocalConfig(ConfigRepository):
    def __init__(self, path: str = "config.json"):
        self.path = path
    def get(self, key: str) -> dict:
        with open(self.path) as f:
            data = json.load(f)
        return data.get(key, {})

class RemoteConfig(ConfigRepository):
    def __init__(self, base_url: str):
        self.base_url = base_url
    def get(self, key: str) -> dict:
        url = f"{self.base_url}/{key}.json"
        return requests.get(url).json()

def get_repo_from_env() -> ConfigRepository:
    backend = os.getenv("CONFIG_BACKEND", "local")
    if backend == "local":
        return LocalConfig()
    elif backend == "http":
        return RemoteConfig(os.getenv("CONFIG_URL", "http://localhost:8000"))
    else:
        raise ValueError(f"Backend desconhecido: {backend}")

repo = get_repo_from_env()
try:
    cfg = repo.get("database")
    print("Configuração obtida:", cfg)
except Exception as e:
    print(f"Erro ao obter configuração: {e}")
