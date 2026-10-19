# unit3-capstone

### STEP 7 RESULTS ###
(venv) du_356058-1790187554@U-3FJ5QDEHXNC01:~/code/ga/unit3-capstone$ python run_capstone.py 
[LOG] query_start: {"trace_id": "52393d68"}
[COST] sql_generation: 301 input tokens, 24 output tokens, cost $0.001263
[COST] sql_interpretation: 41 input tokens, 11 output tokens, cost $0.000288
[COST] synthesis: 99 input tokens, 56 output tokens, cost $0.001137
[LOG] query_complete: {"trace_id": "52393d68", "route": "sql", "sql_validation": "PASSED", "retrieval_chunk_count": 0, "token_usage": {"by_component": {"sql_generation": {"calls": 1, "input": 301, "output": 24, "cost_usd": 0.001263}, "sql_interpretation": {"calls": 1, "input": 41, "output": 11, "cost_usd": 0.000288}, "synthesis": {"calls": 1, "input": 99, "output": 56, "cost_usd": 0.001137}}, "total_cost_usd": 0.002688}}

[rds alone] How many active projects do we have?
 route=sql validation=PASSED
 ## Active Projects

We currently have **4 active projects**.

---

**Source:**
- **Agent:** SQL Agent
- **Query Used:** `SELECT COUNT(*) AS active_project_count FROM projects WHERE status = 'active'`
[LOG] query_start: {"trace_id": "8eefbde7"}
[COST] sql_generation: 303 input tokens, 19 output tokens, cost $0.001194
[COST] sql_interpretation: 48 input tokens, 19 output tokens, cost $0.000429
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|██████████████████████████████████████████████| 103/103 [00:00<00:00, 12615.74it/s]
[COST] retrieval_answer: 2389 input tokens, 89 output tokens, cost $0.008502
[COST] synthesis: 231 input tokens, 222 output tokens, cost $0.004023
[LOG] query_complete: {"trace_id": "8eefbde7", "route": "both", "sql_validation": "PASSED", "retrieval_chunk_count": 5, "token_usage": {"by_component": {"sql_generation": {"calls": 1, "input": 303, "output": 19,"cost_usd": 0.001194}, "sql_interpretation": {"calls": 1, "input": 48, "output": 19, "cost_usd": 0.000429}, "retrieval_answer": {"calls": 1, "input": 2389, "output": 89, "cost_usd": 0.008502}, "synthesis": {"calls": 1, "input": 231, "output": 222, "cost_usd": 0.004023}}, "total_cost_usd": 0.014147999999999999}}

[rds alone] What is the total contract value across all clients?
 route=both validation=PASSED
 ## Total Contract Value Across All Clients

The total contract value across all clients is **$1,515,000**.

---

### Source Attribution

- **SQL Agent** was able to directly answer this question by querying the database:
`SELECT SUM(contract_value) AS total_contract_value FROM clients`
*(Source: SQL database)*

- **Retrieval Agent** was **unable to find** this information within the available documents. While `q2-2026-client-report.pdf` referenced a percentage of contract value spent, no actual dollar amounts or aggregate totals were disclosed in any of the retrieved documents (`remote-work-policy.pdf`, `retail-supply-chain-case-study.pdf`, or `q2-2026-client-report.pdf`).

---

### Key Takeaway
The answer of **$1,515,000** is sourced exclusively from the **SQL Agent's** structured database query and should be considered the authoritative figure for this question.
[LOG] query_start: {"trace_id": "2bb36684"}
[COST] retrieval_answer: 2513 input tokens, 365 output tokens, cost $0.013014
[COST] synthesis: 458 input tokens, 452 output tokens, cost $0.008154
[LOG] query_complete: {"trace_id": "2bb36684", "route": "retrieval", "sql_validation": null, "retrieval_chunk_count": 5, "token_usage": {"by_component": {"retrieval_answer": {"calls": 1, "input": 2513, "output":365, "cost_usd": 0.013014}, "synthesis": {"calls": 1, "input": 458, "output": 452, "cost_usd": 0.008154}}, "total_cost_usd": 0.021168}}

[docs alone] What is our onboarding process?
 route=retrieval validation=n/a
 ## Our Onboarding Process

According to the **Retrieval Agent**, our onboarding process is structured across **four distinct phases**:

---

### 📋 Phase 1: Pre-boarding *(14 Days Before Start Date)*
- Welcome package, employment agreement, and tax documents sent via secure portal *(must be signed 5 daysbefore arrival)*
- IT provisions hardware, email credentials, and permissions *(completed 3 days in advance)*
- Hiring manager appoints an onboarding buddy and prepares a first-week training itinerary

### 🏢 Phase 2: Day One Orientation
- **Morning:** Orientation covering corporate culture, policies, benefits enrollment, and a facilities tour
- **Afternoon:** Hardware setup, login credentials, and multi-factor authentication
- One-on-one with hiring manager to review role expectations and first-month objectives

### 🤝 Phase 3: First Week Integration
- Daily end-of-day check-ins with the hiring manager
- All mandatory compliance modules must be completed by **Day 5**
- Onboarding buddy available for informal questions

### 📈 Phase 4: Long-Term Milestones *(Days 30–90)*
- **Day 30:** Formal review of deliverables with hiring manager
- **Day 60:** Informal feedback review with onboarding buddy
- **Day 90:** Formal performance review + onboarding feedback survey from People Operations

---

### ⚠️ Source Note
This information was sourced by the **Retrieval Agent** from **`Employee Onboarding Process.pdf`**, whichappears to be the directly relevant document. Two additional documents were retrieved (`q2-2026-client-report.pdf` and `cloud-migration-playbook.pdf`), but these do **not** appear relevant to this question and were likely retrieved incidentally. The onboarding details above should be attributed specifically to **`Employee Onboarding Process.pdf`**.
[LOG] query_start: {"trace_id": "b60aa35c"}
[COST] retrieval_answer: 1897 input tokens, 67 output tokens, cost $0.006696
[COST] synthesis: 164 input tokens, 285 output tokens, cost $0.004767
[LOG] query_complete: {"trace_id": "b60aa35c", "route": "retrieval", "sql_validation": null, "retrieval_chunk_count": 5, "token_usage": {"by_component": {"retrieval_answer": {"calls": 1, "input": 1897, "output":67, "cost_usd": 0.006696}, "synthesis": {"calls": 1, "input": 164, "output": 285, "cost_usd": 0.004767}},"total_cost_usd": 0.011463000000000001}}

[docs alone] What is our expense reimbursement policy?
 route=retrieval validation=n/a
 ## Expense Reimbursement Policy

Based on the information retrieved, **I was unable to find an expense reimbursement policy** in the available documents.

### What Was Found:
The **Retrieval Agent** searched the following sources and could not locate a general expense reimbursement policy:

| Source | Relevance |
|--------|-----------|
| `retail-supply-chain-case-study.pdf` | Not relevant to this topic |
| `remote-work-policy.pdf` | Mentions an **equipment stipend**, but no general expense reimbursement policy |
| `q2-2026-client-report.pdf` | Not relevant to this topic |

### Recommendation:
To find our expense reimbursement policy, you may want to:
1. Check with your **HR or Finance department** directly
2. Look in your **employee handbook** or internal HR portal
3. Search for documents specifically titled something like *"Expense Policy"* or *"Travel & Expense Guidelines"*

> ⚠️ *Cited Source: Retrieval Agent | Sources searched: retail-supply-chain-case-study.pdf, remote-work-policy.pdf, q2-2026-client-report.pdf*
[LOG] query_start: {"trace_id": "5dfcf1b0"}
[COST] sql_generation: 309 input tokens, 24 output tokens, cost $0.001287
[COST] sql_interpretation: 49 input tokens, 72 output tokens, cost $0.001227
[COST] retrieval_answer: 2521 input tokens, 344 output tokens, cost $0.012723
[COST] synthesis: 555 input tokens, 512 output tokens, cost $0.009345
[LOG] query_complete: {"trace_id": "5dfcf1b0", "route": "both", "sql_validation": "PASSED", "retrieval_chunk_count": 5, "token_usage": {"by_component": {"sql_generation": {"calls": 1, "input": 309, "output": 24,"cost_usd": 0.001287}, "sql_interpretation": {"calls": 1, "input": 49, "output": 72, "cost_usd": 0.001227}, "retrieval_answer": {"calls": 1, "input": 2521, "output": 344, "cost_usd": 0.012723}, "synthesis": {"calls": 1, "input": 555, "output": 512, "cost_usd": 0.009345}}, "total_cost_usd": 0.024582}}

[both] How many active projects do we have and what's our onboarding process?
 route=both validation=PASSED
 ## Answer

Your question has two parts, which were answered by different agents:

---

### 📊 Active Projects

**You currently have 4 active projects.**

> *Source: **SQL Agent** — queried directly from the database using:*
> `SELECT COUNT(*) AS active_project_count FROM projects WHERE status = 'active'`

*Note: The **Retrieval Agent** referenced only one active client engagement (from the Q2 2026 Quarterly Engagement Report), but this reflects only what was mentioned in the available documents — not the full organizational count. The SQL Agent's result of **4** is the authoritative figure here. [Retrieval Agent Sources 3, 5]*

---

### 🧭 Onboarding Process

The employee onboarding process consists of **four phases**:

1. **Pre-boarding** *(14 days before start date)*
   - Welcome package and documentation sent
   - IT provisions hardware and credentials
   - Hiring manager assigns an onboarding buddy and prepares a training itinerary

2. **Day One Orientation**
   - Morning session with People Operations (culture, policies, benefits, facilities tour)
   - Afternoon IT setup
   - One-on-one meeting with hiring manager

3. **First Week Integration**
   - Daily check-ins with hiring manager
   - Mandatory compliance modules completed by Day 5
   - Buddy support available for informal questions

4. **Long-Term Milestones** *(Months 1–3)*
   - 30-day review with hiring manager
   - 60-day informal buddy check-in
   - 90-day formal performance review + onboarding feedback survey

📌 **Escalation contacts:**
- Technical issues → IT Helpdesk
- HR matters → People Operations
- Role-specific questions → Hiring Manager

> *Source: **Retrieval Agent** — `Employee Onboarding Process.pdf` [Sources 1, 2]*

---

### Summary of Sources Used
| Agent | Source |
|---|---|
| SQL Agent | Live database query |
| Retrieval Agent | `Employee Onboarding Process.pdf`, `q2-2026-client-report.pdf` |
[LOG] query_start: {"trace_id": "b38b0ba8"}
[COST] retrieval_answer: 2514 input tokens, 134 output tokens, cost $0.009552
[COST] synthesis: 240 input tokens, 360 output tokens, cost $0.006120
[LOG] query_complete: {"trace_id": "b38b0ba8", "route": "retrieval", "sql_validation": null, "retrieval_chunk_count": 5, "token_usage": {"by_component": {"retrieval_answer": {"calls": 1, "input": 2514, "output":134, "cost_usd": 0.009552}, "synthesis": {"calls": 1, "input": 240, "output": 360, "cost_usd": 0.00612}},"total_cost_usd": 0.015672}}

[both] Which client has the largest contract, and what does our onboarding process say about new client kickoffs?
 route=retrieval validation=n/a
 ## Answer

Based on the available information retrieved, **neither part of your question can be fully answered** with the documents currently on hand. Here's a breakdown:

---

### 1. Which client has the largest contract?
The **Retrieval Agent** found that the *Q2 2026 Client Report* (**Sources 2 and 3 – q2-2026-client-report.pdf**) does not identify any clients by name or provide contract values in a way that allows comparison across multiple clients. The only contract-related detail available is that **year-to-date spend is at 48% of the annual contract value** for a single, unnamed client. Therefore, **it is not possible to determine which client has the largest contract** from the available documents.

---

### 2. What does our onboarding process say about new client kickoffs?
The **Retrieval Agent** reviewed the onboarding documentation (**Sources 1 and 4 – Employee Onboarding Process.pdf**) and confirmed that it **only covers the employee onboarding process** — there is no mention of client kickoff procedures in any of the retrieved documents.

---

### Recommendation
To answer these questions accurately, you may need to:
- Access a **client contracts database or CRM system** for contract values and client names.
- Locate a **client onboarding or project kickoff document**, separate from the employee onboarding materials.

*Sources cited: Retrieval Agent, Employee Onboarding Process.pdf, q2-2026-client-report.pdf, remote-work-policy.pdf*
[LOG] query_start: {"trace_id": "e5bec209"}
[COST] sql_generation: 301 input tokens, 13 output tokens, cost $0.001098
[LOG] query_complete: {"trace_id": "e5bec209", "route": "sql", "sql_validation": "BLOCKED", "retrieval_chunk_count": 0, "token_usage": {"by_component": {"sql_generation": {"calls": 1, "input": 301, "output": 13,"cost_usd": 0.001098}}, "total_cost_usd": 0.001098}}

[unsafe sql] Delete all projects that are marked completed.
 route=sql validation=BLOCKED
 I was unable to find relevant information to answer this question.
[LOG] query_start: {"trace_id": "c9362663"}
[COST] retrieval_answer: 1876 input tokens, 13 output tokens, cost $0.005823
[COST] synthesis: 109 input tokens, 154 output tokens, cost $0.002637
[LOG] query_complete: {"trace_id": "c9362663", "route": "retrieval", "sql_validation": null, "retrieval_chunk_count": 5, "token_usage": {"by_component": {"retrieval_answer": {"calls": 1, "input": 1876, "output":13, "cost_usd": 0.005823}, "synthesis": {"calls": 1, "input": 109, "output": 154, "cost_usd": 0.002637}},"total_cost_usd": 0.00846}}

[unanswerable] What is the CEO's favorite color?
 route=retrieval validation=n/a
 ## Answer

**The CEO's favorite color is unknown based on available information.**

The Retrieval Agent was unable to find any information regarding the CEO's favorite color after searchingthe available documentation.

**Source:**
- 🔍 **Retrieval Agent** searched the following documents and returned no results:
  - `q2-2026-client-report.pdf`
  - `retail-supply-chain-case-study.pdf`
  - `Employee Onboarding Process.pdf`

This question cannot be answered with the currently available sources. You may want to consult additionalresources, such as internal HR records, executive biographies, or direct communication with the CEO's office.
[LOG] query_start: {"trace_id": "2e93b8f9"}
[COST] sql_generation: 301 input tokens, 15 output tokens, cost $0.001128
[COST] sql_interpretation: 40 input tokens, 11 output tokens, cost $0.000285
[COST] synthesis: 83 input tokens, 49 output tokens, cost $0.000984
[LOG] query_complete: {"trace_id": "2e93b8f9", "route": "sql", "sql_validation": "PASSED", "retrieval_chunk_count": 0, "token_usage": {"by_component": {"sql_generation": {"calls": 1, "input": 301, "output": 15, "cost_usd": 0.001128}, "sql_interpretation": {"calls": 1, "input": 40, "output": 11, "cost_usd": 0.000285}, "synthesis": {"calls": 1, "input": 83, "output": 49, "cost_usd": 0.000984}}, "total_cost_usd": 0.0023970000000000003}}

[extra] How many consultants do we have?
 route=sql validation=PASSED
 ## Answer

We currently have **7 consultants**.

**Source:** This information was retrieved by the **SQL Agent** using the following query:
`SELECT COUNT(*) AS total_consultants FROM consultants`
[LOG] query_start: {"trace_id": "4183ce52"}
[COST] retrieval_answer: 1983 input tokens, 376 output tokens, cost $0.011589
[COST] synthesis: 467 input tokens, 518 output tokens, cost $0.009171
[LOG] query_complete: {"trace_id": "4183ce52", "route": "retrieval", "sql_validation": null, "retrieval_chunk_count": 5, "token_usage": {"by_component": {"retrieval_answer": {"calls": 1, "input": 1983, "output":376, "cost_usd": 0.011589}, "synthesis": {"calls": 1, "input": 467, "output": 518, "cost_usd": 0.009171}}, "total_cost_usd": 0.02076}}

[extra] What is our remote work policy?
 route=retrieval validation=n/a
 ## Acme Consulting Remote Work Policy

Here is a summary of our remote work policy, based on information retrieved from **remote-work-policy.pdf** and **Employee Onboarding Process.pdf** via the **Retrieval Agent**:

---

### 📋 Eligibility
- You must have completed your **90-day probationary period** and your role must not require regular physical presence at a client site.
- Employees **hired as fully remote** are exempt from the 90-day wait, provided it is documented in theiroffer letter.

### 🕐 Core Hours & Availability
- All remote employees must be available **10:00 AM – 3:00 PM in their local time zone**.
- Schedules outside of core hours are flexible, as long as weekly hour expectations are met.

### 💻 Equipment & Security
- The company provides a **laptop, external monitor, and VPN access**.
- Work data must remain on **company-issued devices** — personal cloud storage, personal email, and removable media are not permitted.
- VPN use is **required** on public Wi-Fi.
- Lost or stolen equipment must be reported to IT Security **within four hours**.

### 🏠 Home Office Stipend
- Up to **$500/year** for home office equipment (e.g., desks, chairs, lighting).
- Claims must be submitted by **December 15**; unused amounts **do not roll over**.
- Internet and utility costs are **not covered**.

### ✈️ Working Abroad
- Permitted for up to **20 business days per year**, with manager approval and an IT Security review required.

### 📊 Performance & Review
- Remote work arrangements are reviewed **annually** and can be modified or revoked.
- Employees are given a **30-day improvement window** if issues arise, **except in cases of security violations**.

---

**Sources:** `remote-work-policy.pdf` (Source 1), `Employee Onboarding Process.pdf` (Source 2) — via **Retrieval Agent**

> ⚠️ *Note: A third document, `q2-2026-client-report.pdf`, was retrieved but did not appear to contribute relevant information to this policy summary.*

=== COST SUMMARY ===
retrieval_answer     calls=  7 in= 15693 out=  1388 $0.067899
synthesis            calls=  9 in=  2406 out=  2608 $0.046338
sql_generation       calls=  5 in=  1515 out=    95 $0.005970
sql_interpretation   calls=  4 in=   178 out=   113 $0.002229
Total cost: $0.122436
Most tokens: retrieval_answer
(venv) du_356058-1790187554@U-3FJ5QDEHXNC01:~/code/ga/unit3-capstone$ 

### REFLECTION ###
The question that most tested my orchestrator was "Which client has the largest contract, and what does our onboarding process say about new client kickoffs?" The failure was routing problem: my keyword router didn't recognize "largest" or "contract" as SQL signals, so the question went to the retrieval agent only, and the answer said it couldn't determine the largest contract. A similar misroute send a pure SQL question ("total contract value") to both agents, which cost extra tokens for no benefit. Validation and sysnthesis worked well: the unsafe delete request was blocked, and the synthesizer honestly said when the docs lacked the answer. This shows that multi-agent systems are most fragile at the handoffs. A single scoped agent has no routing decision to get wrong, while here a wrong route produced a plausible but incomplete answer event hough every downstream component worked correctly.