# VIGIL — Data Contracts & Module Communication Specification

**Version:** 0.1  
**Status:** Initial Draft  
**Parent Document:** System Architecture  
**Purpose:** Define standardized data structures exchanged between VIGIL modules.

---

## 1. Introduction

VIGIL consists of multiple logical modules responsible for fault detection, root-cause diagnosis, recovery decision-making, recovery execution, verification and outcome-based learning.

These modules must exchange information using consistent data structures.

This document defines the initial communication contracts for these modules. All modules must follow the field names, data types, formats and validation rules specified here.

### 1.1 General Conventions

| Convention | Standard |
|---|---|
| Data format | JSON |
| API communication | REST |
| Character encoding | UTF-8 |
| Timestamp format | ISO 8601 UTC |
| Timestamp example | `2026-10-31T10:30:00Z` |
| Identifier format | UUID |
| Field naming | snake_case |
| Missing optional values | `null` or omitted, as specified |
| API content type | `application/json` |

All timestamps must represent UTC time and include the timezone indicator.

All identifiers must remain consistent when information moves between modules.

---

# 2. Incident Event Contract

**Producer:** Fault Detection Engine  
**Consumer:** Backend and Diagnosis Engine

### 2.1 Purpose

The Incident Event represents an abnormal condition detected within the distributed application.

It provides the initial information required by VIGIL to investigate a potential failure.

### 2.2 Schema

| Field | Data Type | Required | Description |
|---|---|---|---|
| incident_id | String (UUID) | Yes | Unique incident identifier |
| timestamp | String | Yes | Time of detection in UTC |
| service_id | String | Yes | Identifier of the affected service |
| fault_type | String | Yes | Detected fault category |
| severity | String | Yes | Incident severity |
| observed_metrics | Object | Yes | Relevant measured values |
| health_status | String | Yes | Current health status |
| description | String | Yes | Brief incident description |

### 2.3 Allowed Values

**fault_type**
- SERVICE_UNAVAILABLE
- HIGH_LATENCY
- HIGH_ERROR_RATE
- DEPENDENCY_UNAVAILABLE
- RESOURCE_THRESHOLD_EXCEEDED
- UNKNOWN

**severity**
- LOW
- MEDIUM
- HIGH
- CRITICAL

**health_status**
- HEALTHY
- DEGRADED
- UNHEALTHY
- UNKNOWN

### 2.4 Example JSON

```json
{
  "incident_id": "8f14e45f-ea12-4d9a-9a5b-123456789abc",
  "timestamp": "2026-10-31T10:30:00Z",
  "service_id": "payment-service",
  "fault_type": "SERVICE_UNAVAILABLE",
  "severity": "CRITICAL",
  "observed_metrics": {
    "response_time_ms": 0,
    "error_rate": 1.0,
    "cpu_usage_percent": 0
  },
  "health_status": "UNHEALTHY",
  "description": "Payment service health check failed."
}
```

---

# 3. Service Dependency Contract

**Producer:** Monitoring / Distributed Application Configuration  
**Consumer:** Diagnosis Engine

### 3.1 Purpose

The dependency representation describes relationships between services.

It allows the diagnosis engine to understand which services depend on other services and identify potential upstream causes of failures.

### 3.2 Schema

| Field | Data Type | Required | Description |
|---|---|---|---|
| service_id | String | Yes | Identifier of a service |
| depends_on | Array of Strings | Yes | Services required by this service |

### 3.3 Example JSON

```json
{
  "services": [
    {
      "service_id": "frontend-service",
      "depends_on": ["api-service"]
    },
    {
      "service_id": "api-service",
      "depends_on": ["payment-service", "database-service"]
    },
    {
      "service_id": "payment-service",
      "depends_on": ["database-service"]
    },
    {
      "service_id": "database-service",
      "depends_on": []
    }
  ]
}
```

### 3.4 Interpretation

In this example:

- frontend-service depends on api-service.
- api-service depends on payment-service and database-service.
- payment-service depends on database-service.
- database-service has no declared dependencies.

If database-service becomes unavailable, multiple dependent services may show symptoms.

The diagnosis engine must investigate the dependency relationships before deciding which service is the probable originating cause.

---

# 4. Diagnosis Result Contract

**Producer:** Hierarchical Root-Cause Diagnosis Engine  
**Consumer:** Backend and Recovery Decision Engine

### 4.1 Purpose

The Diagnosis Result communicates the probable originating cause of an incident.

It must distinguish the suspected root cause from services that are merely experiencing propagated symptoms.

### 4.2 Schema

| Field | Data Type | Required | Description |
|---|---|---|---|
| incident_id | String (UUID) | Yes | Associated incident |
| diagnosis_id | String (UUID) | Yes | Unique diagnosis identifier |
| diagnosis_timestamp | String | Yes | Time of diagnosis |
| probable_root_cause | String | Yes | Service identified as probable root cause |
| affected_services | Array of Strings | Yes | Services affected by the incident |
| supporting_evidence | Array of Objects | Yes | Evidence supporting the diagnosis |
| confidence_score | Number | Yes | Confidence between 0 and 1 |
| diagnosis_reasoning | String | Yes | Explanation of the diagnosis |
| diagnosis_method | String | Yes | Method used to reach the conclusion |

### 4.3 Allowed Values

**diagnosis_method**
- RULE_BASED
- STATISTICAL
- MACHINE_LEARNING
- HYBRID

### 4.4 Example JSON

```json
{
  "incident_id": "8f14e45f-ea12-4d9a-9a5b-123456789abc",
  "diagnosis_id": "7a8b9c10-1112-1314-1516-171819202122",
  "diagnosis_timestamp": "2026-10-31T10:30:05Z",
  "probable_root_cause": "database-service",
  "affected_services": [
    "frontend-service",
    "api-service",
    "payment-service",
    "database-service"
  ],
  "supporting_evidence": [
    {
      "service_id": "database-service",
      "observation": "Health check failed",
      "evidence_type": "HEALTH_CHECK"
    },
    {
      "service_id": "api-service",
      "observation": "Database connection attempts failed",
      "evidence_type": "APPLICATION_LOG"
    }
  ],
  "confidence_score": 0.92,
  "diagnosis_reasoning": "The database service is unavailable and multiple dependent services are reporting connection failures. The database is therefore identified as the probable originating cause.",
  "diagnosis_method": "RULE_BASED"
}
```

**Important:** The confidence score is an estimate produced by the diagnosis method. It must not be presented as a statistically calibrated probability unless calibration has actually been implemented and evaluated.

---

# 5. Recovery Request Contract

**Producer:** Recovery Decision Engine  
**Consumer:** Recovery Executor

### 5.1 Purpose

The Recovery Request communicates the selected remediation action to the execution module.

A recommendation does not automatically authorize unrestricted execution. The executor must independently validate the request against its allowlist and safety rules.

### 5.2 Schema

| Field | Data Type | Required | Description |
|---|---|---|---|
| request_id | String (UUID) | Yes | Unique recovery request identifier |
| incident_id | String (UUID) | Yes | Associated incident |
| diagnosis_id | String (UUID) | Yes | Associated diagnosis |
| target_service | String | Yes | Service targeted for recovery |
| action_type | String | Yes | Requested recovery operation |
| action_parameters | Object | Yes | Parameters required for execution |
| justification | String | Yes | Reason for selecting the action |
| safety_validation | Object | Yes | Required safety checks |
| requested_at | String | Yes | Request timestamp |

### 5.3 Initial Allowed Actions

- RESTART_CONTAINER
- RESTART_SERVICE
- NO_ACTION

These are logical action categories. The executor must map them to specific, predefined operations.

### 5.4 Example JSON

```json
{
  "request_id": "11111111-2222-3333-4444-555555555555",
  "incident_id": "8f14e45f-ea12-4d9a-9a5b-123456789abc",
  "diagnosis_id": "7a8b9c10-1112-1314-1516-171819202122",
  "target_service": "database-service",
  "action_type": "RESTART_CONTAINER",
  "action_parameters": {
    "container_name": "vigil-database",
    "timeout_seconds": 30,
    "max_retries": 1
  },
  "justification": "The database service is unavailable and a controlled restart is permitted for this test environment.",
  "safety_validation": {
    "allowlisted": true,
    "test_environment_only": true,
    "approval_required": false
  },
  "requested_at": "2026-10-31T10:30:10Z"
}
```

The safety fields are declarations to be checked, not proof of authorization. The executor must enforce its own environment restrictions, allowlist and execution limits.

---

# 6. Recovery Result Contract

**Producer:** Recovery Executor  
**Consumer:** Backend and Verification Engine

### 6.1 Purpose

The Recovery Result reports whether the requested remediation operation was executed successfully.

Execution success and actual service recovery are separate outcomes.

### 6.2 Schema

| Field | Data Type | Required | Description |
|---|---|---|---|
| request_id | String (UUID) | Yes | Associated recovery request |
| incident_id | String (UUID) | Yes | Associated incident |
| execution_status | String | Yes | Result of execution |
| execution_timestamp | String | Yes | Execution completion time |
| execution_duration_ms | Integer | Yes | Execution duration |
| error_details | String or null | Yes | Error information, if any |

### 6.3 Allowed Values

**execution_status**
- SUCCESS
- FAILED
- TIMEOUT
- REJECTED

### 6.4 Example JSON

```json
{
  "request_id": "11111111-2222-3333-4444-555555555555",
  "incident_id": "8f14e45f-ea12-4d9a-9a5b-123456789abc",
  "execution_status": "SUCCESS",
  "execution_timestamp": "2026-10-31T10:30:40Z",
  "execution_duration_ms": 30000,
  "error_details": null
}
```

A SUCCESS result means that the requested operation completed successfully. It does not establish that the service is healthy again.

---

# 7. Verification Result Contract

**Producer:** Recovery Verification Engine  
**Consumer:** Backend and Outcome Store

### 7.1 Purpose

The Verification Result establishes whether the service recovered after remediation.

### 7.2 Schema

| Field | Data Type | Required | Description |
|---|---|---|---|
| verification_id | String (UUID) | Yes | Unique verification identifier |
| incident_id | String (UUID) | Yes | Associated incident |
| request_id | String (UUID) | Yes | Associated recovery request |
| target_service | String | Yes | Service being verified |
| verification_status | String | Yes | Overall verification outcome |
| health_status | String | Yes | Observed service health |
| verification_timestamp | String | Yes | Time of verification |
| verification_details | String | Yes | Explanation of the result |

### 7.3 Allowed Values

**verification_status**
- RECOVERED
- NOT_RECOVERED
- INCONCLUSIVE

**health_status**
- HEALTHY
- DEGRADED
- UNHEALTHY
- UNKNOWN

### 7.4 Example JSON

```json
{
  "verification_id": "99999999-8888-7777-6666-555555555555",
  "incident_id": "8f14e45f-ea12-4d9a-9a5b-123456789abc",
  "request_id": "11111111-2222-3333-4444-555555555555",
  "target_service": "database-service",
  "verification_status": "RECOVERED",
  "health_status": "HEALTHY",
  "verification_timestamp": "2026-10-31T10:30:50Z",
  "verification_details": "The database health endpoint returned a healthy response after the restart."
}
```

A service that remains unhealthy must not be marked as recovered merely because its container restarted.

---

# 8. Outcome Record

**Producer:** Backend / Outcome Store  
**Consumer:** Learning Component and Recovery Decision Engine

### 8.1 Purpose

The Outcome Record combines information from an incident, diagnosis, recovery attempt and verification result.

It provides historical information for evaluating recovery effectiveness and improving future decisions.

### 8.2 Schema

| Field | Data Type | Required | Description |
|---|---|---|---|
| outcome_id | String (UUID) | Yes | Unique outcome record |
| incident_id | String (UUID) | Yes | Associated incident |
| diagnosis_id | String (UUID) | Yes | Associated diagnosis |
| request_id | String (UUID) | Yes | Associated recovery request |
| verification_id | String (UUID) | Yes | Associated verification |
| root_cause_service | String | Yes | Diagnosed originating service |
| action_type | String | Yes | Executed recovery action |
| recovery_successful | Boolean | Yes | Whether recovery was verified |
| recovery_duration_ms | Integer or null | Yes | Time taken to recover |
| recorded_at | String | Yes | Record timestamp |

### 8.3 Example JSON

```json
{
  "outcome_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
  "incident_id": "8f14e45f-ea12-4d9a-9a5b-123456789abc",
  "diagnosis_id": "7a8b9c10-1112-1314-1516-171819202122",
  "request_id": "11111111-2222-3333-4444-555555555555",
  "verification_id": "99999999-8888-7777-6666-555555555555",
  "root_cause_service": "database-service",
  "action_type": "RESTART_CONTAINER",
  "recovery_successful": true,
  "recovery_duration_ms": 40000,
  "recorded_at": "2026-10-31T10:30:55Z"
}
```

The learning component will analyse historical outcomes and provide information to the recovery decision engine.

It must not assume that an action which succeeded once will always succeed under different conditions.

---

# 9. Data Flow Between Modules

The initial communication sequence is:

1. The monitoring component collects metrics and health information.
2. The fault detection engine identifies an abnormal condition.
3. The detection engine generates an Incident Event.
4. The backend stores the incident and forwards it to the diagnosis engine.
5. The diagnosis engine analyses the incident and dependency information.
6. The diagnosis engine generates a Diagnosis Result.
7. The recovery decision engine evaluates the diagnosis and available historical outcomes.
8. The decision engine generates a Recovery Request.
9. The recovery executor validates and executes the requested action.
10. The executor generates a Recovery Result.
11. The verification engine checks the affected service.
12. The verification engine generates a Verification Result.
13. The backend stores the complete incident and recovery history.
14. The learning component analyses the Outcome Record and supplies historical effectiveness information to future decisions.

---

# 10. Validation Rules

All modules must follow these validation rules:

1. Required fields must not be missing.
2. UUID fields must contain valid UUID values.
3. Timestamps must use ISO 8601 UTC format.
4. Enum fields must use the allowed values defined in this document.
5. Confidence scores must remain between 0 and 1.
6. Execution timeouts and retry counts must have valid non-negative or positive limits as appropriate.
7. Unknown recovery actions must be rejected.
8. A recovery request must reference a valid incident and diagnosis.
9. A verification result must reference the associated recovery request.
10. A recovery operation must never be treated as verified recovery without a successful health check.

---

# 11. Versioning and Change Management

The initial contracts use version 0.1.

Any changes to:
- Field names
- Required fields
- Data types
- Enum values
- Communication flow
- Validation rules

must be discussed before implementation changes are merged.

Future incompatible changes should introduce a new contract version rather than silently modifying existing structures.

---

# 12. Initial Integration Agreement

Every team member must use these shared contracts when developing their assigned module.

| Member | Responsibility | Primary Contract |
|---|---|---|
| Ambuj | Diagnosis, decision and learning | Diagnosis Result, Recovery Request, Outcome Record |
| Parul | Fault detection | Incident Event |
| Stuti | Backend, storage and dashboard | All contracts |
| Vishist | Monitoring and observability | Service Dependency Contract and monitoring data |
| Aviral | Recovery execution and verification | Recovery Request, Recovery Result, Verification Result |

**This document establishes the initial integration agreement for VIGIL.**

The contracts may be refined as implementation progresses, but changes must be coordinated across the team.
