from dotenv import load_dotenv

from mc_monitor_helper_package.auth import get_monte_carlo_auth_from_env
from mc_monitor_helper_package.client import (
    create_or_update_monitors,
    prepare_tables_for_update,
)

load_dotenv()
tables_to_monitor = ["dwh.schema_name.table_name"]

auth = get_monte_carlo_auth_from_env()
prepared_tables = prepare_tables_for_update(
    tablenames_to_monitor=tables_to_monitor, auth=auth, update_monitors=True
)

create_or_update_monitors(
    tables_with_context=prepared_tables,
    fields_to_ignore=["SEQUENCENUMBER", "PK"],
    time_field="SERVERTIME",
    auth=auth,
)
