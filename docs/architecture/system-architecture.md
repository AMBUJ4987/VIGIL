# VIGIL
## System Architecture & Module Interaction Specification

**Document:** Architecture Design — Version 0.1  
**Project:** VIGIL  
**Architecture type:** Modular, locally deployable, hybrid Java–Python system  
**Resource constraint:** Free and open-source software only

---

## 1. Project Overview

VIGIL is an intelligent fault diagnosis and self-healing framework designed for distributed software systems.

Modern applications often consist of multiple interconnected services. A failure in one service can propagate through its dependencies, producing symptoms such as increased latency, failed requests, unavailable endpoints and cascading service disruptions.

Conventional monitoring systems can detect abnormal behaviour and generate alerts, but identifying the originating failure and selecting an appropriate recovery action often requires manual investigation.

VIGIL aims to automate this process through a structured pipeline involving fault detection, hierarchical root-cause diagnosis, recovery decision-making, controlled remediation, recovery verification and outcome-based learning.

The initial implementation will operate in a controlled containerized environment using representative distributed application services and reproducible failure scenarios.

## 2. Architectural Objectives

The architecture must satisfy the following objectives:

1. **Fault visibility:** Collect operational metrics, health information and application logs.
2. **Fault detection:** Identify abnormal service behaviour.
3. **Root-cause diagnosis:** Distinguish originating failures from downstream symptoms.
4. **Recovery selection:** Recommend an appropriate recovery action based on diagnosis and system state.
5. **Controlled execution:** Execute only predefined and authorized recovery operations.
6. **Recovery verification:** Determine whether the attempted recovery restored service health.
7. **Outcome persistence:** Store incident information, diagnoses, actions and recovery results.
8. **Outcome-based learning:** Use historical recovery outcomes to improve future decisions.
9. **Reproducibility:** Support repeatable experiments and measurable evaluation.
10. **Resource efficiency:** Run locally using free software and ordinary computing hardware.

## 3. High-Level Architecture

The system consists of the following logical components:

1. Distributed Application Environment
2. Monitoring and Observability
3. Fault Detection Engine
4. Hierarchical Root-Cause Diagnosis Engine
5. Recovery Decision Engine
6. Recovery Executor
7. Recovery Verification Engine
8. Outcome Store and Learning Component
9. Backend API and Dashboard

### 3.1 Processing Pipeline

Distributed Application → Monitoring → Fault Detection → Root-Cause Diagnosis → Recovery Decision → Recovery Execution → Recovery Verification → Outcome Storage and Learning.

The outcome-learning component provides feedback to future recovery decisions.

The dashboard provides visibility into incidents, diagnoses, recovery operations and historical outcomes.

## 4. Component Architecture and Responsibilities

### 4.1 Distributed Application Environment

**Purpose:** Provide the test environment in which VIGIL observes and manages failures.

Responsibilities:
- Host multiple interconnected application services.
- Expose health-check endpoints.
- Generate application metrics and logs.
- Support controlled fault injection.
- Simulate realistic service dependencies.

Initial scope:
- At least two interconnected services.
- One service acting as a dependency of another.
- Representative failures such as service crashes, increased latency and dependency unavailability.

Technology: Java/Python sample services, Docker Engine and Docker Compose.

### 4.2 Monitoring and Observability

**Purpose:** Collect operational information about the distributed application.

Responsibilities:
- Collect service-level metrics.
- Monitor service availability.
- Track request latency and error rates.
- Expose health-check results.
- Make application logs accessible to the detection component.

Technology:
- Prometheus for metrics collection.
- Application health endpoints.
- Structured application logs.

Prometheus is responsible for metrics collection; application logs will initially be handled separately.

### 4.3 Fault Detection Engine

**Purpose:** Identify abnormal conditions in monitored services.

Responsibilities:
- Evaluate incoming metrics and health information.
- Detect service unavailability.
- Identify unusual latency and error rates.
- Generate structured incident events.
- Attach timestamps, affected services and relevant observations.

Initial implementation:
- Threshold-based and rule-based detection.
- Configurable thresholds.
- Reproducible fault scenarios for testing.

The detection component identifies a potential fault. It does not independently determine the final root cause.

### 4.4 Hierarchical Root-Cause Diagnosis Engine

**Purpose:** Identify the probable originating cause of an incident by analysing service dependencies and observed symptoms.

This is a core intelligence component owned by the project lead.

Responsibilities:
- Analyse incident information.
- Examine service dependencies.
- Identify affected and upstream services.
- Distinguish primary failures from propagated symptoms.
- Assign probable root causes.
- Provide a confidence or evidence score.
- Explain the reasoning behind each diagnosis.

Initial implementation:
- Dependency-aware rule-based diagnosis.
- Hierarchical analysis of affected services.
- Evidence-based prioritization of probable root causes.

Future enhancement:
- Statistical analysis of historical incidents.
- Learning from previously verified diagnoses.
- Improved diagnosis ranking.

### 4.5 Recovery Decision Engine

**Purpose:** Select a suitable recovery action based on the diagnosis and current system state.

Responsibilities:
- Receive the diagnosis result.
- Examine available recovery actions.
- Consider historical recovery outcomes.
- Check action eligibility and safety constraints.
- Recommend an appropriate recovery action.
- Provide a reason for the recommendation.

Initial implementation:
- Rule-based action selection.
- Predefined action catalogue.
- Recovery eligibility checks.

Future enhancement:
- Outcome-informed action ranking.
- Statistical evaluation of action effectiveness.
- Adaptive recovery recommendations.

### 4.6 Recovery Executor

**Purpose:** Execute an approved recovery operation.

Responsibilities:
- Receive an authorized recovery request.
- Validate the requested action.
- Execute only allowlisted operations.
- Apply execution timeouts and retry limits.
- Return a structured execution result.

Initial implementation:
- Restart a designated test service or container.
- Return success, failure or timeout status.

Safety restrictions:
- No unrestricted shell execution.
- No arbitrary host-level commands.
- No modification of production systems.
- No execution of actions outside the predefined allowlist.

### 4.7 Recovery Verification Engine

**Purpose:** Determine whether the recovery operation successfully restored the affected service.

Responsibilities:
- Check service health after remediation.
- Verify that the service responds correctly.
- Evaluate recovery within a defined time window.
- Distinguish successful, failed and inconclusive recovery attempts.
- Generate a structured verification result.

A successful command execution must not automatically be considered a successful recovery. Actual service health must be checked.

### 4.8 Outcome Store and Learning Component

**Purpose:** Preserve recovery history and use previous outcomes to improve future decisions.

Responsibilities:
- Store incident details.
- Store diagnosis results.
- Record selected and executed recovery actions.
- Record verification results.
- Associate recovery attempts with their outcomes.
- Analyse historical recovery effectiveness.
- Provide outcome-informed information to the decision engine.

Initial implementation:
- PostgreSQL for persistent records.
- Python for statistical analysis and learning logic.
- Rule-based recovery decisions as the initial baseline.

The learning component will initially be lightweight and explainable. Complex machine-learning models are not a requirement for the first working implementation.

### 4.9 Backend API and Dashboard

**Purpose:** Coordinate communication between system components and provide visibility into system operation.

Responsibilities:
- Expose APIs for incident and recovery data.
- Coordinate communication between the detection, diagnosis and recovery components.
- Persist system records.
- Provide access to historical incidents.
- Display service status, diagnoses and recovery outcomes.

Technology:
- Java and Spring Boot for the central backend.
- PostgreSQL for persistence.
- HTML, CSS and JavaScript for the initial dashboard.

## 5. Inter-Module Communication

The system will use REST APIs and JSON-based communication between logical components.

The following contracts define the initial integration boundaries.

### 5.1 Incident Event

Generated by the fault detection component.

Expected fields:
- incident_id
- timestamp
- service_id
- fault_type
- severity
- observed_metrics
- health_status
- description

### 5.2 Diagnosis Result

Generated by the diagnosis engine.

Expected fields:
- incident_id
- probable_root_cause
- affected_services
- supporting_evidence
- confidence_score
- diagnosis_reasoning

### 5.3 Recovery Request

Generated by the recovery decision engine.

Expected fields:
- incident_id
- target_service
- action_type
- action_parameters
- justification
- safety_validation
- request_id

### 5.4 Recovery Result

Generated by the recovery executor.

Expected fields:
- request_id
- execution_status
- execution_timestamp
- execution_duration
- error_details

### 5.5 Verification Result

Generated by the recovery verification component.

Expected fields:
- incident_id
- target_service
- verification_status
- health_status
- verification_timestamp
- verification_details

These are initial logical contracts. Exact JSON types, validation rules, enumerations and API endpoints will be finalized in Milestone 2.

## 6. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Main backend | Java + Spring Boot | APIs and orchestration |
| Intelligence | Python + scikit-learn | Diagnosis and learning |
| Python API | FastAPI | Communication with Python modules |
| Database | PostgreSQL | Persistent storage |
| Monitoring | Prometheus | Metrics collection |
| Visualization | Grafana OSS | Monitoring dashboards |
| Containers | Docker Engine / Docker Compose | Local deployment |
| Frontend | HTML, CSS, JavaScript | User interface |
| Version control | Git + GitHub | Collaboration |

All selected technologies have free-to-use options suitable for the proposed local educational implementation. Applicable open-source licences and Docker usage terms must be respected.

No paid APIs, cloud infrastructure, commercial datasets or paid AI services are required.

## 7. Proposed Repository Structure

```text
VIGIL/
│
├── backend/
│   ├── src/
│   └── README.md
│
├── diagnosis/
│   ├── root_cause/
│   └── README.md
│
├── learning/
│   ├── models/
│   └── README.md
│
├── fault-detection/
│   ├── rules/
│   └── README.md
│
├── recovery/
│   ├── executor/
│   └── README.md
│
├── monitoring/
│   ├── prometheus/
│   └── README.md
│
├── docker/
│   ├── compose.yaml
│   └── README.md
│
├── dashboards/
│
├── tests/
│
└── docs/
    ├── architecture/
    ├── design/
    └── research/
```

The exact structure may be adjusted as modules are implemented.

## 8. System Safety and Reliability

VIGIL must operate within explicit safety boundaries.

1. Automated recovery is restricted to the controlled test environment.
2. Every recovery action must be predefined and allowlisted.
3. Recovery requests must be validated before execution.
4. Execution timeouts and retry limits must be enforced.
5. Recovery success must be established through health verification.
6. Failed or inconclusive recovery attempts must be recorded.
7. Historical learning must not bypass recovery safety restrictions.
8. The system must retain an auditable record of decisions and actions.

## 9. Initial Implementation Strategy

The project will be developed incrementally.

**Phase 1 — Infrastructure**
- Create the distributed test application.
- Configure Docker Compose.
- Establish monitoring and health checks.
- Implement fault injection.

**Phase 2 — Intelligence**
- Implement incident processing.
- Develop hierarchical root-cause diagnosis.
- Implement the initial recovery decision engine.

**Phase 3 — Remediation**
- Implement controlled recovery execution.
- Add post-recovery verification.
- Record recovery outcomes.

**Phase 4 — Learning**
- Build historical recovery analysis.
- Develop an initial outcome-informed decision mechanism.
- Compare its performance against the rule-based baseline.

**Phase 5 — Integration and Evaluation**
- Integrate all modules.
- Build the dashboard.
- Execute reproducible experiments.
- Measure detection, diagnosis and recovery performance.

## 10. Evaluation Metrics

VIGIL will be evaluated using measurable criteria:

- Fault detection time.
- Root-cause diagnosis accuracy.
- Recovery decision accuracy.
- Mean time to recovery (MTTR).
- Recovery success rate.
- Unnecessary recovery interventions.
- Outcome-learning improvement over the initial rule-based baseline.

Evaluation will use controlled failure scenarios and recorded ground-truth information.

## 11. Architectural Limitations and Future Scope

The initial implementation will focus on a small controlled distributed environment. It will not claim to support arbitrary production infrastructure.

Potential future extensions include:
- More sophisticated anomaly detection.
- Graph-based root-cause analysis.
- Additional recovery strategies.
- More advanced outcome-learning algorithms.
- Larger service dependency graphs.
- Container orchestration integration.

These extensions will be considered only after the initial system is functional and measurable.

## 12. Conclusion

VIGIL is designed as a modular, intelligent and safety-constrained framework for fault diagnosis and automated recovery in distributed software systems.

Its architecture separates monitoring, fault detection, diagnosis, recovery decision-making, execution, verification and learning into clearly defined responsibilities.

The initial implementation prioritizes explainability, reproducibility, low resource consumption and complete local operation. This provides a practical foundation for incremental development while leaving room for more advanced intelligence and automation.
