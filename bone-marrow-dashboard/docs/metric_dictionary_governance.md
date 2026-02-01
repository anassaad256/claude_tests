# Bone Marrow Service Operations Dashboard
## Metric Dictionary & Governance Memo

**Document Version:** 1.0
**Effective Date:** [INSERT DATE]
**Document Owner:** Hematopathology Fellow
**Approved By:** Hematopathology Section/Department Head

---

## 1. Purpose & Scope

### 1.1 Purpose
This document defines the metrics, data sources, calculation methods, targets, and governance framework for the Bone Marrow Service Operations Dashboard. The dashboard provides standardized operational visibility to identify avoidable delays and support ongoing QA/QI discussions.

### 1.2 Scope
| Included | Excluded |
|----------|----------|
| Bone marrow cases signed out by hematopathology service | Lymph node cases |
| Adult and Pediatric cases (reported separately) | Patient identifiers (PHI) |
| Flow cytometry timing (as external dependency) | Cytogenetics/FISH/molecular result tracking |
| CoPath workflow fields only | Send-out results beyond flow cytometry |

### 1.3 Population Definitions
- **Adult Cases:** Patients aged 18 years or older at time of procedure
- **Pediatric Cases:** Patients under 18 years at time of procedure

---

## 2. Metric Definitions

### 2.1 Volume Metrics

| Metric | Definition | Data Source | Calculation |
|--------|------------|-------------|-------------|
| **Adult Bone Marrow Volume** | Count of adult bone marrow cases signed out during the reporting period | CoPath case export | COUNT of cases WHERE patient_age >= 18 AND specimen_type = 'bone marrow' AND sign_out_date WITHIN reporting period |
| **Pediatric Bone Marrow Volume** | Count of pediatric bone marrow cases signed out during the reporting period | CoPath case export | COUNT of cases WHERE patient_age < 18 AND specimen_type = 'bone marrow' AND sign_out_date WITHIN reporting period |

### 2.2 Turnaround Time (TAT) Metrics

| Metric | Definition | Unit | Calculation |
|--------|------------|------|-------------|
| **Primary TAT** | Time from case accession to final hematopathology sign-out | Calendar days | sign_out_datetime - accession_datetime |
| **TAT Median** | 50th percentile of Primary TAT | Calendar days | PERCENTILE(Primary TAT, 0.50) |
| **TAT P90** | 90th percentile of Primary TAT | Calendar days | PERCENTILE(Primary TAT, 0.90) |
| **TAT % Within Target** | Percentage of cases meeting TAT target | Percentage | (COUNT cases WHERE Primary TAT <= target) / (Total cases) × 100 |

**Notes:**
- TAT calculation uses calendar days (not business days) for consistency
- Partial days are rounded to one decimal place
- Cases without sign-out dates are excluded from TAT calculations

### 2.3 Flow Dependency Metrics

| Metric | Definition | Unit | Calculation |
|--------|------------|------|-------------|
| **Flow Dependency Time** | Time from accession to flow cytometry result available/verified in CoPath | Calendar days | flow_result_datetime - accession_datetime |
| **Flow Median** | 50th percentile of Flow Dependency Time | Calendar days | PERCENTILE(Flow Dependency Time, 0.50) |
| **Flow P90** | 90th percentile of Flow Dependency Time | Calendar days | PERCENTILE(Flow Dependency Time, 0.90) |

**Notes:**
- Flow cytometry is a send-out service; timing reflects external lab performance
- Cases without flow cytometry orders are excluded from these metrics
- If flow result timestamp is unavailable, use date of result verification in CoPath

### 2.4 Service Responsiveness (Lag) Metrics

| Metric | Definition | Unit | Calculation |
|--------|------------|------|-------------|
| **Service Lag** | Time from flow cytometry result available to final sign-out | Calendar days | sign_out_datetime - flow_result_datetime |
| **Lag Median** | 50th percentile of Service Lag | Calendar days | PERCENTILE(Service Lag, 0.50) |
| **Lag P90** | 90th percentile of Service Lag | Calendar days | PERCENTILE(Service Lag, 0.90) |
| **Lag % Within Target** | Percentage of cases meeting lag target | Percentage | (COUNT cases WHERE Service Lag <= target) / (Total cases with flow) × 100 |

**Notes:**
- This metric isolates internal service performance from external dependencies
- Only applicable to cases with flow cytometry orders
- Negative values (sign-out before flow result) should be flagged for data quality review

### 2.5 Quality Proxy Metrics

| Metric | Definition | Unit | Data Source |
|--------|------------|------|-------------|
| **Amended/Corrected Count** | Number of reports with amendments or corrections | Count | CoPath amendment tracking field |
| **Amendment Rate** | Percentage of cases with amendments | Percentage | (Amended cases / Total cases) × 100 |
| **TAT Outliers** | Cases exceeding the outlier threshold | Count | COUNT cases WHERE Primary TAT > outlier_threshold |

### 2.6 Outlier Driver Categories

For TAT outliers, assign primary driver based on the following logic:

| Driver Category | Definition | Assignment Logic |
|-----------------|------------|------------------|
| **Flow Cytometry Delay** | Delay primarily attributable to external flow lab | Flow Dependency Time > expected AND Service Lag <= target |
| **Internal Service Lag** | Delay primarily attributable to internal sign-out process | Flow Dependency Time <= expected AND Service Lag > target |
| **Processing/Technical Issues** | Delay due to specimen processing, staining, or technical problems | Documented processing issue OR significant delay before flow order |
| **Other/Multiple Factors** | Multiple contributing factors or unclear attribution | Does not fit other categories OR multiple factors documented |

---

## 3. Targets & Thresholds

### 3.1 Performance Targets

| Metric | Target | Source/Rationale |
|--------|--------|------------------|
| **Primary TAT** | ≤ 3 calendar days | [Align with section expectations - CONFIRM] |
| **TAT % Within Target** | ≥ 90% | Standard laboratory performance expectation |
| **Service Lag** | ≤ 1 calendar day | Internal responsiveness goal |
| **Lag % Within Target** | ≥ 90% | Standard laboratory performance expectation |

### 3.2 Alert Thresholds

| Performance Level | Threshold | Dashboard Display | Action Required |
|-------------------|-----------|-------------------|-----------------|
| **Target Met** | ≥ 90% of target | Green | Continue monitoring |
| **Near Target** | 75-89% of target | Yellow/Amber | Enhanced monitoring, investigate trends |
| **Below Target** | < 75% of target | Red | Root cause analysis required |

### 3.3 Outlier Definition
- **TAT Outlier Threshold:** > 7 calendar days (cases requiring driver attribution)
- Threshold subject to adjustment based on baseline performance

---

## 4. Data Sources & Collection

### 4.1 Primary Data Source
**CoPath/LIS Operational Export**
- Limited to workflow fields only
- Fields extracted:
  - Case identifier (for interval calculation only - removed from final dataset)
  - Specimen type
  - Patient age category (Adult/Pediatric - no DOB)
  - Accession date/time
  - Flow result date/time (if applicable)
  - Sign-out date/time
  - Amendment indicator
  - Signing pathologist (optional - for workload analysis)

### 4.2 PHI Handling Protocol
1. Accession numbers used only for:
   - Linking timestamps across data fields
   - Calculating time intervals
2. Accession numbers are REMOVED before:
   - Final dataset creation
   - Dashboard generation
   - Any distribution or storage
3. Final dataset contains only aggregate statistics
4. No patient name, MRN, DOB, or other direct identifiers extracted

### 4.3 Data Collection Schedule
| Activity | Frequency | Responsible Party | Deadline |
|----------|-----------|-------------------|----------|
| Data export from CoPath | Monthly | Fellow / LIS Support | 5th business day of following month |
| Data processing & validation | Monthly | Fellow | 7th business day of following month |
| Dashboard generation | Monthly | Fellow | 10th business day of following month |

---

## 5. Exclusions & Special Cases

### 5.1 Standard Exclusions
- Cases accessioned but not signed out by month end (captured in subsequent month)
- Test/training cases
- Cancelled cases
- Cases signed out by non-hematopathology service

### 5.2 Handling Special Cases
| Scenario | Handling |
|----------|----------|
| Case re-signed to different pathologist | Use final sign-out timestamp |
| Multiple bone marrow specimens same case | Count as single case; use final sign-out |
| Preliminary report issued | Use final sign-out timestamp only |
| Case transferred to/from another institution | Exclude from TAT metrics; count in volume if signed out by service |

---

## 6. Governance & Review

### 6.1 Roles & Responsibilities

| Role | Responsibility |
|------|----------------|
| **Hematopathology Fellow (Project Lead)** | Data extraction, dashboard generation, preliminary analysis, presentation |
| **Hematopathology Faculty Reviewer** | Dashboard review, interpretation guidance, approval for distribution |
| **Section/Department Head (Sponsor)** | Strategic oversight, resource allocation, escalation decisions |
| **AP Lab Manager** | Operational context, process improvement support |
| **CoPath/LIS Support** | Technical support for data exports, field definitions |
| **Send-out Flow Coordinator** | External flow cytometry timing context (as needed) |

### 6.2 Review Cadence

| Forum | Frequency | Participants | Purpose |
|-------|-----------|--------------|---------|
| Fellow-Faculty Review | Monthly | Fellow, Faculty Reviewer | Dashboard review, data validation, preliminary analysis |
| Section QA Meeting | Monthly or Quarterly | Section faculty, Fellow | Formal review, trend analysis, action planning |
| Department Quality Meeting | Quarterly | Department leadership, Section rep | Aggregate reporting, escalation of systemic issues |

### 6.3 Action Threshold Protocol

**When thresholds are exceeded:**
1. Document finding in dashboard notes section
2. Conduct brief root cause discussion at next review
3. Identify actionable factors (internal vs. external)
4. Document action items with owner and target date
5. Track action item completion at subsequent reviews

### 6.4 Change Control
- Process changes identified through dashboard review follow existing departmental/lab change control procedures
- Metric definitions or target changes require Section Head approval
- Changes to this document require version update and re-approval

---

## 7. Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [DATE] | [Fellow Name] | Initial version |

---

## Appendix A: Sample Data Export Template

```
Fields for CoPath Export Request:
1. case_id (temporary - for linking only)
2. specimen_type
3. patient_age_category (Adult/Pediatric)
4. accession_datetime
5. flow_order_datetime (if applicable)
6. flow_result_datetime (if applicable)
7. signout_datetime
8. amendment_flag (Y/N)
9. amendment_count
10. signing_pathologist_id (optional)
```

## Appendix B: Dashboard Distribution List

| Recipient | Format | Frequency |
|-----------|--------|-----------|
| Section Faculty | PDF via email / shared drive | Monthly |
| Department Quality Committee | PDF summary | Quarterly |
| Lab Manager | PDF via email | Monthly |

---

*This document is reviewed annually or when significant changes to metrics or processes occur.*
