# VIGIL
### Intelligent Fault Diagnosis and Self-Healing for Distributed Systems

<p align="center">
  <strong>Detect. Diagnose. Recover. Learn.</strong>
</p>

VIGIL is an intelligent self-healing framework designed to improve the reliability and resilience of distributed software systems through automated fault detection, hierarchical root-cause diagnosis, controlled recovery, and outcome-based learning.

Modern distributed applications consist of multiple interconnected services. A failure in one component can propagate across dependent services, causing increased latency, service disruptions, and reduced system reliability. Traditional monitoring solutions can identify abnormal behaviour but often rely on manual investigation and intervention to resolve failures.

VIGIL aims to reduce this dependency on manual intervention by combining system observability, intelligent diagnosis, automated remediation, and learning from previous recovery outcomes.

---

## Objectives

- **Fault Detection:** Identify abnormal system behaviour using operational metrics, application logs, and service health information.
- **Hierarchical Diagnosis:** Analyse service dependencies and failure indicators to identify probable root causes.
- **Intelligent Recovery Selection:** Determine suitable corrective actions based on diagnostic results and current system conditions.
- **Automated Remediation:** Execute predefined recovery procedures within controlled safety constraints.
- **Recovery Verification:** Evaluate whether the executed recovery action successfully restores acceptable system behaviour.
- **Outcome-Based Learning:** Record previous recovery attempts and use their outcomes to improve future recovery decisions.

## System Architecture

The proposed VIGIL architecture follows a structured fault-management pipeline:

```text
       Distributed Application
                 |
                 v
          Monitoring Layer
          (Metrics and Logs)
                 |
                 v
           Fault Detection
                 |
                 v
       Hierarchical Diagnosis
                 |
                 v
         Recovery Selection
                 |
                 v
        Remediation Executor
                 |
                 v
        Recovery Verification
                 |
                 v
          Outcome Learning
                 |
                 v
       Historical Outcome Store
                 |
                 +------> Future Recovery Decisions
```

A centralized dashboard will provide visibility into system health, detected incidents, diagnostic results, recovery actions, and historical outcomes.

## Core Components

| Component | Responsibility |
|---|---|
| Monitoring Layer | Collects operational metrics, logs, and service health information. |
| Fault Detection | Identifies abnormal conditions and generates incident events. |
| Hierarchical Diagnosis | Analyses service dependencies to determine probable root causes. |
| Recovery Decision Engine | Selects suitable recovery actions based on diagnosis and system state. |
| Remediation Executor | Executes approved recovery actions under predefined safety constraints. |
| Recovery Verification | Checks whether the system has recovered successfully. |
| Outcome Learning | Uses historical recovery outcomes to improve future decisions. |
| Dashboard | Displays system health, incidents, diagnosis results, and recovery history. |

## Proposed Technology Stack

The project is being developed using free and open-source technologies.

| Category | Technology |
|---|---|
| Backend | Java, Spring Boot |
| Intelligence and Diagnosis | Python |
| Machine Learning | scikit-learn |
| Containerization | Docker, Docker Compose |
| Monitoring | Prometheus |
| Visualization | Grafana |
| Database | PostgreSQL |
| Frontend | HTML, CSS, JavaScript |
| Version Control | Git, GitHub |

*The technology stack is subject to refinement during development.*

## Development Approach

VIGIL will initially be implemented in a controlled, containerized environment using representative failure scenarios.

The development process will follow these stages:

1. Establish a distributed application environment.
2. Configure monitoring and telemetry collection.
3. Implement controlled fault-injection scenarios.
4. Develop fault detection and hierarchical diagnosis.
5. Implement recovery selection and safety constraints.
6. Develop automated remediation and recovery verification.
7. Introduce outcome-based learning.
8. Integrate the dashboard and historical storage.
9. Evaluate the system against conventional monitoring and rule-based recovery approaches.

## Evaluation Criteria

The system will be evaluated using measurable performance indicators, including:

- Fault Detection Time
- Root-Cause Diagnosis Accuracy
- Recovery Time
- Recovery Success Rate
- Unnecessary Recovery Interventions
- Effectiveness of Outcome-Based Learning

The evaluation will investigate whether hierarchical diagnosis and outcome-aware recovery decisions improve the effectiveness of automated fault recovery.

## Project Scope

The initial implementation focuses on a controlled distributed environment and a predefined set of representative failure scenarios.

Automated recovery actions will operate under explicit safety constraints. The project prioritizes explainability, reproducibility, measurable outcomes, and practical feasibility.

## Repository Structure

```text
VIGIL/
│
├── docs/
│   ├── architecture/
│   ├── design/
│   └── research/
│
├── monitoring/
├── fault-detection/
├── diagnosis/
├── recovery/
├── learning/
│
├── backend/
├── dashboard/
├── tests/
│
├── docker/
│   └── docker-compose.yml
│
├── README.md
├── LICENSE
└── .gitignore
```

*Directories will be populated as the corresponding modules are developed.*

## Project Team

| Member | Responsibility |
|---|---|
| Ambuj | Project Lead & Intelligence Core |
| Parul | Fault Detection & Experimentation |
| Stuti | Backend Integration, Storage & Dashboard |
| Vishist | Monitoring & Observability |
| Aviral | Recovery Executor & Verification |

## Current Status

**Status:** Under Development

VIGIL is currently in its initial development phase. The team is establishing the distributed test environment, defining module interfaces, and implementing the foundational components.

## License

This project is licensed under the **Apache License 2.0**.

See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>VIGIL</strong><br/>
  <em>Building systems that can detect, diagnose, and recover from their own failures.</em>
</p>
