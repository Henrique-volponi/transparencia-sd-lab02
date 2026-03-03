import os
import requests

SERVICE_REGISTRY = {
    "user-service":    os.getenv("USER_SERVICE_URL",    "http://localhost:8080"),
    "product-service": os.getenv("PRODUCT_SERVICE_URL", "http://localhost:9090"),
}

class ServiceLocator:
    def __init__(self, registry):
        self.registry = registry
    def resolve(self, name):
        return self.registry.get(name)

locator = ServiceLocator(SERVICE_REGISTRY)

def buscar_usuario(user_id: int) -> dict:
    base = locator.resolve("user-service")
    url = f"{base}/users/{user_id}"
    try:
        return requests.get(url, timeout=2).json()
    except Exception as e:
        return {"erro": str(e)}

def buscar_produto(prod_id: int) -> dict:
    base = locator.resolve("product-service")
    url = f"{base}/products/{prod_id}"
    try:
        return requests.get(url, timeout=2).json()
    except Exception as e:
        return {"erro": str(e)}

print("URL resolvida para user-service:", locator.resolve("user-service"))
print("Resultado da busca:", buscar_usuario(1))
