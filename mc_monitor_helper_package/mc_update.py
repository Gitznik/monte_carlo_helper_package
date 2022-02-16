from typing import Dict, List

from mc_monitor_helper_package.api_functions import query_mc_api
from mc_monitor_helper_package.auth import MonteCarloAuth
from mc_monitor_helper_package.mc_table import MonteCarloTableContext
from mc_monitor_helper_package.queries import MonitorSetter


def set_monitor(
    auth: MonteCarloAuth,
    table_with_context: MonteCarloTableContext,
    fields: List[str],
    time_field: str,
    monitor_type: str = "stats",
    schedule_config: Dict = {"scheduleType": "LOOSE", "intervalMinutes": 720},
) -> None:
    query_mc_api(
        auth=auth,
        executable=MonitorSetter(
            mcon=table_with_context.mcon,
            fields=fields,
            time_axis_type=table_with_context.timefields[time_field],
            time_axis_name=time_field,
            monitor_type=monitor_type,
            schedule_config=schedule_config,
        ),
    )
