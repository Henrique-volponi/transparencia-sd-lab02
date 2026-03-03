import time
import random
from enum import Enum

class CBState(Enum):
    CLOSED    = "closed"
    OPEN      = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=3.0):
        self.state = CBState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = None
    def call(self, func, *args, **kwargs):
        now = time.time()
        if self.state == CBState.OPEN:
            if now - self.last_failure_time > self.recovery_timeout:
                self.state = CBState.HALF_OPEN
            else:
                print("Circuito aberto! Falha rápida.")
                return None
        try:
            result = func(*args, **kwargs)
            self.failure_count = 0
            if self.state == CBState.HALF_OPEN:
                self.state = CBState.CLOSED
            return result
        except Exception as e:
            self.failure_count += 1
            print(f"Falha detectada: {e}")
            if self.failure_count >= self.failure_threshold:
                self.state = CBState.OPEN
                self.last_failure_time = now
            return None

def servico_externo(user_id: int) -> dict:
    if random.random() < 0.7:
        raise Exception("Falha no serviço externo!")
    return {"id": user_id, "nome": "Usuario Teste"}

cb = CircuitBreaker(failure_threshold=3, recovery_timeout=3.0)

print("=== Simulando 10 chamadas ao servico externo ===\n")
for i in range(10):
    resultado = cb.call(servico_externo, i)
    print(f"Chamada {i}: {resultado}")
    time.sleep(0.3)
