import random
from typing import List
from dataclasses import dataclass, field

class FakeConnection:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.alive = True
    def query(self, sql: str):
        if not self.alive:
            raise ConnectionError(f"Conexão perdida: {self.dsn}")
        print(f"[{self.dsn}] Executando: {sql}")
        return f"result_{random.randint(1,100)}"

def connect(dsn: str) -> FakeConnection:
    if "bad" in dsn:
        raise ConnectionError(f"Falha ao conectar: {dsn}")
    return FakeConnection(dsn)

@dataclass
class ReplicaPool:
    master_dsn: str
    replica_dsns: List[str]
    _master: FakeConnection = field(init=False)
    _replicas: List[FakeConnection] = field(init=False)
    _healthy: List[FakeConnection] = field(init=False)

    def __post_init__(self):
        self._master = connect(self.master_dsn)
        self._replicas = [connect(dsn) for dsn in self.replica_dsns]
        self._healthy = self._replicas.copy()

    def query(self, sql: str, write: bool = False):
        if write:
            return self._master.query(sql)
        else:
            if not self._healthy:
                print("Nenhuma réplica saudável, lendo do master!")
                return self._master.query(sql)
            replica = random.choice(self._healthy)
            try:
                return replica.query(sql)
            except ConnectionError:
                print(f"Replica {replica.dsn} falhou, removendo do pool.")
                self._healthy.remove(replica)
                return self.query(sql, write=write)

pool = ReplicaPool(
    master_dsn="postgresql://app@master:5432/app",
    replica_dsns=[
        "postgresql://app@replica1:5432/app",
        "postgresql://app@replica2:5432/app",
        "postgresql://app@bad-replica:5432/app"
    ]
)

print("=== Leituras (com balanceamento entre replicas) ===")
for i in range(5):
    pool.query(f"SELECT * FROM users WHERE id={i + 1}")

print("\n=== Escrita (sempre no master) ===")
pool.query("INSERT INTO logs VALUES ('evento')", write=True)

print(f"\nReplicas saudaveis restantes: {len(pool._healthy)}")
