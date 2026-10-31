# VIGIL — Hierarchical Root-Cause Diagnosis Design

**Version:** 0.1  
**Component Owner:** Project Lead  
**Implementation Language:** Python  
**Component Type:** Dependency-Aware Diagnostic Intelligence

---

## 1. Introduction

The Hierarchical Root-Cause Diagnosis Engine is a core intelligence component of VIGIL.

Its purpose is to identify the probable originating cause of a distributed system incident by analysing service dependencies, observed failures and supporting operational evidence.

In distributed systems, an individual service failure may affect multiple dependent services. These dependent services may exhibit errors, increased latency or unavailability even when they are not independently faulty.

The diagnosis engine must therefore distinguish between originating failures and propagated symptoms.

The proposed initial implementation uses dependency-aware graph analysis combined with explainable rule-based reasoning.

## 2. Objectives

The diagnosis engine must:

1. Analyse incident information received from the fault detection module.
2. Represent service relationships using a directed dependency graph.
3. Identify affected services.
4. Examine upstream and downstream failure relationships.
5. Identify candidate root causes.
6. Aggregate evidence supporting each candidate.
7. Rank probable root causes.
8. Generate an explainable diagnosis result.
9. Handle ambiguous and incomplete observations.
10. Communicate its output using the standardized VIGIL Diagnosis Result contract.

## 3. Input Requirements

The diagnosis engine receives:

- Incident Event.
- Service Dependency Contract.
- Relevant service health information.
- Available operational evidence.

Evidence may include:
- Health-check failures.
- Application error messages.
- Connection failures.
- Response-time anomalies.
- Service availability information.
- Incident timestamps.

The engine must validate incoming information before beginning diagnosis.

## 4. Dependency Graph Representation

The distributed application will be represented as a directed graph.

Each node represents an individual service.

Each directed edge represents a dependency relationship.

For example:

```text
Frontend → API
API → Payment
API → Database
Payment → Database
```

The direction indicates that the service on the left depends on the service on the right.

The graph allows the diagnosis engine to traverse service relationships and identify potential failure propagation paths.

A service with multiple dependent services may cause widespread disruption if it fails.

## 5. Proposed Diagnosis Pipeline

The engine will follow these stages.

### Stage 1: Input Validation

Validate:
- Incident identifier.
- Affected service identifier.
- Fault category.
- Timestamp.
- Dependency information.
- Evidence structure.

Invalid or incomplete inputs must be handled explicitly.

### Stage 2: Dependency Graph Construction

Construct a directed graph from the service dependency information.

Validate the graph for:
- Unknown service references.
- Duplicate relationships.
- Self-dependencies.
- Cyclic dependencies.

Cyclic relationships must be handled rather than silently ignored.

### Stage 3: Affected Service Identification

Identify services associated with the incident.

Determine which services are:
- Directly observed as unhealthy.
- Indirectly affected through dependencies.
- Currently healthy.
- Of unknown health status.

### Stage 4: Dependency Analysis

Examine relationships between affected services.

For each unhealthy service, inspect its dependencies.

Determine whether:
- The service has an unhealthy dependency.
- Multiple failures share a common upstream dependency.
- The service has independent failure evidence.
- The observed failure could be propagated from another service.

### Stage 5: Candidate Root-Cause Generation

Generate a list of possible root-cause services.

Candidates should be selected using:
- Direct failure observations.
- Dependency relationships.
- Supporting operational evidence.
- Temporal ordering, where reliable timestamps are available.

A service must not be considered a root cause merely because it has the highest number of dependent services.

### Stage 6: Evidence Aggregation and Ranking

Evaluate each candidate using available evidence.

Possible evidence categories:

| Evidence | Interpretation |
|---|---|
| Failed health check | Direct evidence of service unavailability |
| Connection refusal | Possible dependency failure |
| Application error | Supporting evidence |
| High latency | Possible degradation |
| Earlier failure timestamp | Potentially useful causal evidence |
| Multiple downstream failures | Evidence of possible propagation |

The initial implementation will use transparent rule-based scoring.

Each candidate will receive a diagnostic ranking score based on the available evidence.

The score must be explainable and must not be presented as a calibrated probability.

### Stage 7: Diagnosis Generation

Produce a Diagnosis Result containing:

- Incident identifier.
- Diagnosis identifier.
- Probable root cause.
- Affected services.
- Supporting evidence.
- Confidence or ranking score.
- Diagnosis explanation.
- Diagnosis method.

If the evidence is insufficient, the engine must report uncertainty instead of inventing a definite root cause.

## 6. Initial Algorithm Strategy

The first implementation will use dependency-aware rule-based reasoning.

Proposed logic:

1. Receive the incident and service dependency graph.
2. Identify unhealthy services.
3. Find upstream dependencies of each unhealthy service.
4. Identify shared dependencies across multiple unhealthy services.
5. Examine direct failure evidence for each candidate.
6. Evaluate whether downstream symptoms are consistent with dependency propagation.
7. Rank candidates using evidence.
8. Select a probable root cause when sufficient evidence exists.
9. Return an uncertain diagnosis when evidence is insufficient.

This implementation will serve as the explainable baseline for future enhancements.

## 7. Ambiguous and Incomplete Cases

The engine must account for situations in which:

- Multiple services fail independently.
- A service fails without any unhealthy dependencies.
- Dependency information is incomplete.
- Timestamps are unavailable or unreliable.
- Multiple candidate root causes have similar evidence.
- A dependency is degraded but not unavailable.
- A monitoring component reports conflicting information.

The engine should support multiple candidate diagnoses and an inconclusive result.

It must not force a single root cause when the evidence does not justify one.

## 8. Output Contract

The engine must generate the standardized VIGIL Diagnosis Result.

Required fields:

- incident_id
- diagnosis_id
- diagnosis_timestamp
- probable_root_cause
- affected_services
- supporting_evidence
- confidence_score
- diagnosis_reasoning
- diagnosis_method

The output must remain compatible with the data-contracts specification.

## 9. Initial Implementation Technologies

| Technology | Purpose |
|---|---|
| Python | Core diagnosis implementation |
| NetworkX | Dependency graph representation and traversal |
| Pydantic | Input/output validation |
| Pytest | Unit and integration testing |

All selected libraries are available without paid subscriptions.

## 10. Testing Strategy

The engine will be evaluated using controlled service failure scenarios.

Initial test cases:

**Scenario 1 — Single Service Failure**

One service fails without any dependency failure.

Expected result: Identify the directly failing service as the probable root cause.

**Scenario 2 — Upstream Dependency Failure**

A database fails and multiple dependent services become unhealthy.

Expected result: Identify the database as the probable originating cause when supported by the evidence.

**Scenario 3 — Independent Failures**

Two unrelated services fail independently.

Expected result: Identify multiple candidate root causes rather than incorrectly combining them.

**Scenario 4 — Incomplete Evidence**

A service is unhealthy but dependency information is missing.

Expected result: Report uncertainty and insufficient evidence.

**Scenario 5 — Multiple Candidate Causes**

Multiple upstream services show failure evidence.

Expected result: Rank candidates and provide supporting explanations.

**Scenario 6 — Cyclic Dependency Information**

The supplied dependency graph contains a cycle.

Expected result: Detect and report the invalid or unsupported dependency structure without entering an infinite traversal.

## 11. Evaluation Metrics

The diagnosis engine will be evaluated using:

- Root-cause identification accuracy.
- Precision.
- Recall.
- F1-score.
- False root-cause identification rate.
- Diagnosis processing time.
- Performance under incomplete evidence.

Ground-truth information from controlled fault injection experiments will be used to evaluate the results.

## 12. Future Enhancements

Potential future improvements include:

- Temporal dependency analysis.
- Statistical evidence aggregation.
- Graph-based root-cause ranking.
- Historical incident comparison.
- Outcome-informed diagnostic improvements.
- Machine-learning-assisted diagnosis.

These enhancements will be introduced only after the rule-based baseline is implemented and evaluated.

## 13. Conclusion

The VIGIL Hierarchical Root-Cause Diagnosis Engine is designed to identify probable originating failures in distributed applications by analysing service dependencies and operational evidence.

Its initial implementation prioritizes explainability, deterministic behaviour, reproducibility and compatibility with the broader VIGIL architecture.

The component will establish the diagnostic foundation upon which the recovery decision and outcome-learning mechanisms will operate.