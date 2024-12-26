from dataclasses import dataclass

@dataclass
class Config:
    host: str = "localhost"
    port: int = 5432
    database: str = "project_orders_management"
    user: str = "postgres"
    password: str = "12345678"
