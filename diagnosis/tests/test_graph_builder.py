import pytest

from diagnosis.root_cause.graph_builder import (
    build_graph,
    validate_graph,
    get_dependencies,
    get_dependents,
    get_upstream_services,
    get_downstream_services,
    get_topological_order,
    GraphValidationError,
)


SAMPLE_DATA = {
    "services": [
        {
            "service_id": "frontend",
            "depends_on": ["api"]
        },
        {
            "service_id": "api",
            "depends_on": ["payment", "database"]
        },
        {
            "service_id": "payment",
            "depends_on": ["database"]
        },
        {
            "service_id": "database",
            "depends_on": []
        }
    ]
}


def test_graph_creation():
    graph = build_graph(SAMPLE_DATA)

    assert graph.number_of_nodes() == 4
    assert graph.number_of_edges() == 4


def test_direct_dependencies():
    graph = build_graph(SAMPLE_DATA)

    assert set(get_dependencies(graph, "api")) == {
        "payment",
        "database"
    }


def test_direct_dependents():
    graph = build_graph(SAMPLE_DATA)

    assert set(get_dependents(graph, "database")) == {
        "api",
        "payment"
    }


def test_transitive_dependencies():
    graph = build_graph(SAMPLE_DATA)

    assert set(get_upstream_services(graph, "frontend")) == {
        "api",
        "payment",
        "database"
    }


def test_transitive_dependents():
    graph = build_graph(SAMPLE_DATA)

    assert set(get_downstream_services(graph, "database")) == {
        "frontend",
        "api",
        "payment"
    }


def test_dependency_first_order():
    graph = build_graph(SAMPLE_DATA)
    order = get_topological_order(graph)

    assert order.index("database") < order.index("api")
    assert order.index("api") < order.index("frontend")


def test_unknown_dependency():
    invalid_data = {
        "services": [
            {
                "service_id": "api",
                "depends_on": ["missing-service"]
            }
        ]
    }

    assert validate_graph(invalid_data)


def test_circular_dependency():
    invalid_data = {
        "services": [
            {
                "service_id": "api",
                "depends_on": ["database"]
            },
            {
                "service_id": "database",
                "depends_on": ["api"]
            }
        ]
    }

    with pytest.raises(GraphValidationError):
        build_graph(invalid_data)


def test_unknown_service_query():
    graph = build_graph(SAMPLE_DATA)

    with pytest.raises(ValueError):
        get_dependencies(graph, "unknown-service")