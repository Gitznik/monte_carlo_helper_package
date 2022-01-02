import pytest
from mc_monitor_helper_package.mc_table import MonteCarloTable


@pytest.fixture
def test_table() -> MonteCarloTable:
    return MonteCarloTable(database="db", schema="schema_name", table_name="table")


def test_name_creation(test_table: MonteCarloTable):
    assert test_table.full_table_name == "db:schema_name.table"
