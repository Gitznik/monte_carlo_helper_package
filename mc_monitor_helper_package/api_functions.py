from typing import Optional, Protocol

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from auth import MonteCarloAuth


class ApiExecutable(Protocol):
    query: str
    params: dict

    def parse_response(self, response: dict) -> dict:
        ...


def query_mc_api(
    auth: MonteCarloAuth,
    executable: ApiExecutable,
) -> dict:
    transport = RequestsHTTPTransport(
        url="https://api.getmontecarlo.com/graphql",
        headers=auth.auth_headers,
    )
    query = gql(executable.query)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    return client.execute(query, variable_values=executable.params)
