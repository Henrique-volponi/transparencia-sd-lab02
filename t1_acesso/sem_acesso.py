import json
import requests

def ler_configuracao(origem: str):
    if origem == "local":
        with open("config.json") as f:
            return json.load(f)
    elif origem == "http":
        url = "http://localhost:8000/config.json"
        return requests.get(url).json()
    elif origem == "s3":
        # Simulação: normalmente usaria boto3
        raise NotImplementedError("Acesso S3 não implementado neste exemplo")
    else:
        raise ValueError(f"Origem desconhecida: {origem}")

try:
    cfg = ler_configuracao("local")
    print("Configuração carregada:", cfg)
except FileNotFoundError:
    print("config.json não encontrado — crie um para testar")
