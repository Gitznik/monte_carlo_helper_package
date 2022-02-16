from dataclasses import dataclass
from typing import List

from mc_monitor_helper_package.exceptions import NoNewMonitorsFound


@dataclass
class MonteCarloTable:
    database: str
    schema: str
    table_name: str

    @property
    def full_table_name(self) -> str:
        return str.lower(f"{self.database}:{self.schema}.{self.table_name}")

    def __repr__(self) -> str:
        return self.full_table_name


def parse_tables(tables_to_monitor: List[str]) -> list:
    return [
        MonteCarloTable(
            database=table_to_monitor.split(".")[0],
            schema=table_to_monitor.split(".")[1],
            table_name=table_to_monitor.split(".")[2],
        )
        for table_to_monitor in tables_to_monitor
    ]


def parse_mc_table(table: str) -> MonteCarloTable:
    table_to_monitor = table.replace(":", ".")
    return MonteCarloTable(
        database=table_to_monitor.split(".")[0],
        schema=table_to_monitor.split(".")[1],
        table_name=table_to_monitor.split(".")[2],
    )


def find_tables_without_monitor(
    database_tables: List[MonteCarloTable],
    tables_with_monitor: List[MonteCarloTable],
) -> List[MonteCarloTable]:
    tables_with_monitor = [
        table for table in database_tables if table not in tables_with_monitor
    ]
    if len(tables_with_monitor) == 0:
        raise NoNewMonitorsFound("No new tables to monitor")
    return tables_with_monitor
