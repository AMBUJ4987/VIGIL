from typing import Any

import networkx as nx


class GraphValidationError(ValueError):
    """Raised when the service dependency graph is invalid."""


def validate_graph(dependency_data: dict[str, Any]) -> list[str]:
    """
    Validate a VIGIL service dependency definition.

    Expected format:
    {
        "services": [
            {
                "service_id": "api-service",
                "depends_on": ["database-service"]
            }
        ]
    }

    Returns a list of validation errors.
    An empty list means the definition is valid.
    """

    errors = []

    if not isinstance(dependency_data, dict):
        return ["Dependency data must be a JSON object."]

    services = dependency_data.get("services")

    if not isinstance(services, list):
        return ["'services' must be a list."]

    service_ids = set()

    # First pass: validate service definitions and collect IDs.
    for index, service in enumerate(services):
        if not isinstance(service, dict):
            errors.append(f"Service at index {index} must be an object.")
            continue

        service_id = service.get("service_id")

        if not isinstance(service_id, str) or not service_id.strip():
            errors.append(
                f"Service at index {index} has an invalid service_id."
            )
            continue

        if service_id in service_ids:
            errors.append(f"Duplicate service_id: '{service_id}'")
        else:
            service_ids.add(service_id)

        dependencies = service.get("depends_on")

        if not isinstance(dependencies, list):
            errors.append(
                f"'depends_on' for '{service_id}' must be a list."
            )
            continue

        if not all(
            isinstance(dependency, str) and dependency.strip()
            for dependency in dependencies
        ):
            errors.append(
                f"'depends_on' for '{service_id}' "
                "must contain non-empty strings."
            )
            continue

        if len(dependencies) != len(set(dependencies)):
            errors.append(
                f"Duplicate dependencies found for '{service_id}'."
            )

        if service_id in dependencies:
            errors.append(
                f"Service '{service_id}' cannot depend on itself."
            )

    if errors:
        return errors

    # Second pass: check whether every dependency exists.
    for service in services:
        service_id = service["service_id"]

        for dependency in service["depends_on"]:
            if dependency not in service_ids:
                errors.append(
                    f"Unknown dependency '{dependency}' "
                    f"referenced by '{service_id}'."
                )

    if errors:
        return errors

    # Third pass: construct a temporary graph to check cycles.
    graph = nx.DiGraph()
    graph.add_nodes_from(service_ids)

    for service in services:
        for dependency in service["depends_on"]:
            graph.add_edge(service["service_id"], dependency)

    if not nx.is_directed_acyclic_graph(graph):
        cycles = list(nx.simple_cycles(graph))

        for cycle in cycles:
            errors.append(
                "Circular dependency detected: "
                + " -> ".join(cycle + [cycle[0]])
            )

    return errors


def build_graph(dependency_data: dict[str, Any]) -> nx.DiGraph:
    """
    Build and return a validated directed service dependency graph.

    Edge convention:
        A -> B means A depends on B.
    """

    errors = validate_graph(dependency_data)

    if errors:
        raise GraphValidationError(
            "Invalid service dependency graph:\n- "
            + "\n- ".join(errors)
        )

    graph = nx.DiGraph()

    for service in dependency_data["services"]:
        service_id = service["service_id"]

        graph.add_node(service_id)

        for dependency in service["depends_on"]:
            graph.add_edge(service_id, dependency)

    return graph


def get_dependencies(
    graph: nx.DiGraph,
    service_id: str
) -> list[str]:
    """Return the direct dependencies of a service."""

    _check_service(graph, service_id)

    return list(graph.successors(service_id))


def get_dependents(
    graph: nx.DiGraph,
    service_id: str
) -> list[str]:
    """Return services that directly depend on this service."""

    _check_service(graph, service_id)

    return list(graph.predecessors(service_id))


def get_upstream_services(
    graph: nx.DiGraph,
    service_id: str
) -> list[str]:
    """
    Return all transitive dependencies of a service.

    These are services reachable by following dependency edges.
    """

    _check_service(graph, service_id)

    return list(nx.descendants(graph, service_id))


def get_downstream_services(
    graph: nx.DiGraph,
    service_id: str
) -> list[str]:
    """
    Return all transitive dependents of a service.

    These are services that depend on this service,
    either directly or through another service.
    """

    _check_service(graph, service_id)

    return list(nx.ancestors(graph, service_id))


def get_topological_order(graph: nx.DiGraph) -> list[str]:
    """
    Return services in dependency-first order.

    Dependencies appear before the services that require them.
    """

    if not nx.is_directed_acyclic_graph(graph):
        raise GraphValidationError(
            "Cannot calculate topological order: graph contains a cycle."
        )

    return list(reversed(list(nx.topological_sort(graph))))


def _check_service(graph: nx.DiGraph, service_id: str) -> None:
    """Ensure that a requested service exists in the graph."""

    if service_id not in graph:
        raise ValueError(
            f"Service '{service_id}' does not exist in the dependency graph."
        )