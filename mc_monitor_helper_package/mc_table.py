from dataclasses import dataclass


@dataclass
class MonteCarloTable:
    database: str
    schema: str
    table_name: str

    @property
    def full_table_name(self) -> str:
        return str.lower(f"{self.database}:{self.schema}.{self.table_name}")
