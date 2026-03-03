import multiprocessing
import time
import os
from dotenv import load_dotenv
import redis

load_dotenv()

def get_redis() -> redis.Redis:
    return redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        password=os.getenv("REDIS_PASSWORD"),
        decode_responses=True
    )

def inicializar_saldo(valor: int = 1000):
    r = get_redis()
    r.set("lab06:saldo", valor)
    print(f"Saldo inicial: R${valor}")

def transferir_sem_lock(valor: int, nome: str):
    r = get_redis()
    saldo = int(r.get("lab06:saldo"))
    time.sleep(0.1)
    novo_saldo = saldo - valor
    r.set("lab06:saldo", novo_saldo)
    print(f"  [{nome}] transferiu R${valor}. Saldo registrado: R${novo_saldo}")

if __name__ == "__main__":
    inicializar_saldo(1000)
    p1 = multiprocessing.Process(target=transferir_sem_lock, args=(300, "A"))
    p2 = multiprocessing.Process(target=transferir_sem_lock, args=(200, "B"))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    saldo_final = int(get_redis().get("lab06:saldo"))
    print(f"Perda por race condition: R${500 - saldo_final}")
