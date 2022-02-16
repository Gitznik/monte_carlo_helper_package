from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from mc_monitor_helper_package.mc_table import MonteCarloTable, parse_mc_table


@dataclass
class WarehouseIdGetter:
    query: str = """
        query getUser {
        getUser {
            account {
            warehouses {
                uuid
                connectionType
            }
            }
        }
        }
    """

    @property
    def params(self) -> None:
        return

    @staticmethod
    def parse_response(response: dict) -> Optional[str]:
        return response["getUser"]["account"]["warehouses"][0]["uuid"]


@dataclass
class ExistingMonitorGetter:
    user_defined_monitor_types: Optional[list]
    query: str = """
        query getAllUserDefinedMonitors($userDefinedMonitorTypes: [String], $first: Int, $cursor: String) {
        getAllUserDefinedMonitorsV2(userDefinedMonitorTypes: $userDefinedMonitorTypes, first: $first, after: $cursor) {
            pageInfo {
            startCursor
            endCursor
            hasNextPage
            hasPreviousPage
            __typename
            }
            edges {
            node {
                __typename
                id
                monitorType
                entities
                customRuleEntities: entities
            }
            __typename
            }
            __typename
        }
        }
        """

    @property
    def params(self) -> dict:
        return {
            "userDefinedMonitorTypes": self.user_defined_monitor_types,
        }

    @staticmethod
    def parse_response(response: dict) -> List[MonteCarloTable]:
        return [
            parse_mc_table(monitor["node"]["customRuleEntities"][0])
            for monitor in response["getAllUserDefinedMonitorsV2"]["edges"]
        ]


@dataclass
class MconsForTablesGetter:
    full_table_id: str
    dw_id: str
    is_timefield: str
    query: str = """
        query getTable($dwId: UUID, $fullTableId: String, $mcon: String, $isTimeField: Boolean, $isTextField: Boolean, $isNumericField: Boolean, $cursor: String, $versions: Int = 1, $first: Int = 20) {
        getTable(dwId: $dwId, fullTableId: $fullTableId, mcon: $mcon) {
            id
            mcon
            fullTableId
            versions(first: $versions) {
            edges {
                node {
                fields(first: $first, isTimeField: $isTimeField, isTextField: $isTextField, isNumericField: $isNumericField, after: $cursor) {
                    edges {
                    node {
                        name
                        fieldType
                        isTimeField
                        __typename
                    }
                    __typename
                    }
                    __typename
                }
                __typename
                }
                __typename
            }
            __typename
            }
            __typename
        }
        }
    """

    @property
    def params(self) -> dict:
        return {
            "fullTableId": self.full_table_id,
            "dwId": self.dw_id,
            "isTimeField": self.is_timefield,
        }

    @staticmethod
    def parse_response(response: dict) -> Tuple[str, Dict]:
        mcon = response["getTable"]["mcon"]
        timefields = {
            node["node"]["name"]: node["node"]["fieldType"]
            for node in response["getTable"]["versions"]["edges"][0]["node"]["fields"][
                "edges"
            ]
        }
        return mcon, timefields


@dataclass
class MonitorSetter:
    mcon: None
    fields: None
    time_axis_type: None
    time_axis_name: None
    monitor_type: str = "stats"
    schedule_config: dict
    query: str = """
        mutation createMonitor($mcon: String!, $monitorType: String!, $fields: [String], $timeAxisName: String, $timeAxisType: String, $scheduleConfig: ScheduleConfigInput, $whereCondition: String) {
        createMonitor(mcon: $mcon, monitorType: $monitorType, fields: $fields, timeAxisName: $timeAxisName, timeAxisType: $timeAxisType, scheduleConfig: $scheduleConfig, whereCondition: $whereCondition) {
            monitor {
            entities
            fields
            type
            timeAxisFieldName
            timeAxisFieldType
            __typename
            }
            __typename
        }
        }
    """

    @property
    def params(self) -> dict:
        return {
            "mcon": self.mcon,
            "monitorType": self.monitor_type,
            "fields": self.fields,
            "timeAxisName": self.time_axis_name,
            "timeAxisType": self.time_axis_type,
            "scheduleConfig": self.schedule_config,
        }

    @staticmethod
    def parse_response(response: Dict) -> Dict:
        return response
