# Finance Team Utilization Tracker
### Enterprise Record-to-Report (R2R) Capacity & Workload Governance Platform

A production-grade **Weekly Employee Utilization Tracker** engineered for Finance Shared Services and Record-to-Report (R2R) operations in multinational enterprise environments (SAP BPC, SAP Group Reporting, close cycles, intercompany, statutory audits, and controls).

---

## 🚀 Quick Start (Single-Click Windows Launcher)

The application includes a pre-configured Windows launcher:

1. Double-click **`Run_Utilization_Tracker.bat`** in the repository root.
2. The script will automatically:
   - Verify Python 3.11+
   - Create required directories (`data/`, `logs/`, `exports/`)
   - Install dependencies from `requirements.txt`
   - Launch Streamlit and open the app at `http://localhost:8501`

*(Alternatively, run from PowerShell / Terminal: `streamlit run app.py`)*

---

## 🔐 Default Login Credentials

The system seeds an Administrator account on initial boot. When realistic demo data is seeded, leadership and employee accounts are provisioned:

| Role | Employee ID | Default Password | Scope / Permissions |
| :--- | :--- | :--- | :--- |
| **Admin** | `EMP001` | `admin123` | System settings, user master, lock weeks, backups, demo seeder |
| **Director** | `EMP002` | `demo123` | All teams, Director executive dashboard, PowerPoint deck export |
| **Team Lead (R2R)** | `EMP003` | `demo123` | Record-to-Report team view, management dashboard, reminders |
| **Team Lead (Reporting)**| `EMP004` | `demo123` | Financial Reporting & BPC team view & management dashboard |
| **Employee** | `EMP010` | `demo123` | Weekly entry, personal history, live utilization |

*Note: All passwords are encrypted with bcrypt (12 rounds). First login can prompt a mandatory password change.*

---

## 📐 Mathematical Formulation & Worked Examples

### 1. Fundamental Baseline
$$\text{Standard Daily Hours} = 7.5 \text{ hours/day (configurable)}$$
$$\text{Working Days (Week)} = (\text{Mon–Fri Working Days}) - (\text{Public Holidays in Employee Location})$$

### 2. Available Capacity
$$\text{Available Hours (Week)} = \max\left(0, (\text{Working Days} - \text{Leave Days Entered}) \times 7.5\right)$$
- Regular leave (Casual, Sick, Comp-off) **reduces available hours**, keeping utilization fair for employees taking legitimate leave.

### 3. Excluded Week Rule (Maternity, Sabbatical, Full-Week Leave)
If an employee is on approved long-term leave (Maternity/Paternity, Sabbatical, Long-term Medical) or takes leave $\ge$ working days:
- $\text{Available Hours} = 0$
- **Both numerator and denominator are dropped** from weekly, monthly, and yearly aggregation.
- The week never counts as 0% and does not drag down team or annual averages. In the UI and reports, it is rendered as `Excluded – <Leave Type>`.

### 4. Weekly Utilization Rate & Critical Overload Rule
$$\text{Utilization \% (Week)} = \frac{\text{Total Logged Hours}}{\text{Available Hours}} \times 100$$

> **CRITICAL ARCHITECTURAL RULE**:  
> **NEVER block, cap, or reject hours because utilization exceeds 100%.**  
> In multinational finance operations, employees routinely log 50–70 hours during month-end or quarter-end close. The system displays a non-blocking amber informational notice (e.g., *"Logged hours exceed available hours (136.7%)"*) and flags the overload tier for management review, but **never restricts entry**.

#### Worked Example:
- **Scenario**: Employee with 5 working days in a standard week takes **1 day of casual leave** and logs **41 hours** during month-end close.
- **Available Hours**: $(5 - 1) \times 7.5 = \mathbf{30.0 \text{ hours}}$
- **Logged Hours**: $\mathbf{41.0 \text{ hours}}$
- **Utilization \%**: $\frac{41.0}{30.0} \times 100 = \mathbf{136.7\%}$
- **System Behavior**: Entry accepted without restriction; prominent card indicates **136.7%**; non-blocking amber notice flags **Critical Overload (>120%)**; capacity gap = $-11.0\text{ hrs}$ (overload).

### 5. Hours-Weighted Aggregation (Never Average of Percentages)
A common flaw in rudimentary trackers is calculating monthly utilization as the simple arithmetic average of weekly percentages:
$$\text{Naive Average (INCORRECT)} = \frac{100\% + 200\%}{2} = 150.0\%$$
The system strictly enforces **hours-weighted aggregation**:
$$\text{Enterprise Utilization (CORRECT)} = \frac{\sum \text{Included Logged Hours}}{\sum \text{Included Available Hours}} \times 100$$

#### Numerical Proof:
- **Week 1 (Light week)**: 10 hours logged on 10 available hours = $100\%$
- **Week 2 (Close peak)**: 50 hours logged on 25 available hours = $200\%$
- **Total Logged**: $10 + 50 = 60\text{ hours}$
- **Total Available**: $10 + 25 = 35\text{ hours}$
- **True Utilization**: $\frac{60}{35} \times 100 = \mathbf{171.4\%} \neq 150.0\%$

### 6. Threshold Tiers & Burnout Detection
- `< 70.0%`: Under-utilized (Red)
- `70.0% – 85.0%`: Below Target (Amber)
- `85.0% – 100.0%`: Optimal (Green)
- `> 100.0%`: **Burnout Overload** (Dark Red)
  - `100.0% – 110.0%`: **Watch Tier**
  - `110.0% – 120.0%`: **High Tier**
  - `> 120.0%`: **Critical Tier**

---

## 🗂️ The 9 Finance Activity Categories (Fixed Order)

| # | Code | Category Name | Classification | Primary Nature |
| :-: | :--- | :--- | :--- | :--- |
| **1** | `CLOSE` | Period-End Close (Month/Quarter/Year) | **BAU** | Journal entries, accruals, cut-off, trial balance |
| **2** | `REPORTING`| Financial Reporting (BPC & Group Reporting) | **BAU** | Consolidation packages, intercompany reconciliation |
| **3** | `RECON` | Account Reconciliations | **BAU** | Balance sheet balance reconciliations, BlackLine |
| **4** | `INTERCO` | Intercompany | **BAU** | Cross-border invoicing, dispute matching, settlement |
| **5** | `AUDIT` | Audit, Control & Compliance | **BAU** | Internal & external statutory audit samples, SOX |
| **6** | `CI_AUTO` | Continuous Improvement & Automation | **VALUE-ADD** | PowerQuery, Python, Alteryx, VBA, process sprints |
| **7** | `GOVERNANCE`| Stakeholder Management & Governance | **VALUE-ADD** | Controllership reviews, operating committees |
| **8** | `ADHOC` | Ad-hoc & Special Projects | **VALUE-ADD** | M&A integrations, ERP migrations, special carve-outs |
| **9** | `FPNA` | Planning & Forecasting | **BAU** | Budgets, quarterly revised estimates, cash forecast |

---

## 🏗️ Architecture & Data Model

```
Capstone_1/
├── app.py                         # Application entry, login, 60-min timeout, role routing
├── requirements.txt               # Pinned dependencies
├── Run_Utilization_Tracker.bat    # Windows 1-click launcher
├── core/
│   ├── auth.py                    # Bcrypt hashing, role hierarchy, permission checks
│   ├── calc.py                    # Pure calculation functions, burnout logic, aggregation
│   ├── calendar.py                # Monday-Sunday weeks, holidays, fiscal year, close-day math
│   ├── data_service.py            # Relational queries, cascading filters, high-speed telemetry
│   ├── db.py                      # SQLAlchemy models, SQLite engine, schema initialization
│   ├── export_excel.py            # 8-sheet Excel workbook generator with styles & formulas
│   ├── export_pptx.py             # 8-slide executive PowerPoint deck generator
│   ├── insights.py                # Rule-based executive narrative generation
│   ├── seed_data.py               # 52-week realistic demo seeder & 1-click wiper
│   └── ui_components.py           # Reusable CSS, KPI cards, badges, global filters
├── pages/
│   ├── 1_Weekly_Entry.py          # Fast hours grid, leave section, live card, amber banner
│   ├── 2_My_History.py            # Employee self-service trends, mix charts, log history
│   ├── 3_Team_View.py             # Team lead compliance, member allocations, team donuts
│   ├── 4_Management_Dashboard.py  # Manager KPIs, heatmap, team matrix, exception audits
│   ├── 5_Director_Dashboard.py    # Executive review, close curves, automation ROI, PPTX export
│   ├── 6_Exports.py               # 8-sheet Excel workbook, templates, bulk uploads
│   └── 7_Admin.py                 # User/team masters, settings, week locks, backups, seeder
├── tests/
│   └── test_calc.py               # Pytest suite for calculation engine
└── data/
    └── tracker.db                 # SQLite database (auto-generated)
```

### Relational Schema
- `users`: `(id, emp_id, name, email, role, password_hash, location_id, join_date, exit_date, is_active, must_change_pw)`
- `teams`: `(id, name, lead_user_id, function, cost_centre, is_active)`
- `user_teams`: `(user_id, team_id, is_primary)`
- `categories`: `(id, code, name, type [BAU|VALUE_ADD], sort_order, color, is_active)`
- `leave_types`: `(id, name, excluded_from_utilization, is_system)`
- `holidays`: `(id, location_id, date, name)`
- `weekly_entries`: `(id, user_id, week_start, status, comment, submitted_at, locked)`
- `weekly_leaves`: `(entry_id, leave_type_id, days)`
- `weekly_hours`: `(entry_id, team_id, category_id, hours)`
- `targets`: `(team_id, category_id, target_mix_pct, target_util_pct, fy)`
- `automation_savings`: `(month_year, team_id, hours_saved, description)`
- `settings`: `(key, value)`
- `audit_log`: `(id, user_id, action, table_name, record_id, old_value, new_value, ts)`

---

## 🧪 Unit Testing

Execute the comprehensive test suite with `pytest`:
```bash
python -m pytest tests/ -v
```
All 13 pure-function unit tests validate:
- Normal 37.5-hour weeks at 100%
- Worked example: 1 day casual leave + 41 hrs logged = 136.7% critical overload
- Full-week leave dropped from numerator and denominator
- Maternity leave multi-week exclusion
- Public holiday weeks with reduced working days
- Burnout severity tiers (Watch 100-110%, High 110-120%, Critical >120%)
- Month straddling prorating vs ISO Thursday rule
- Hours-weighted aggregation vs naive average
- Zero-available hours edge cases
- Multi-team split attribution
- Fiscal year calendar (Jan-Dec) vs Financial year (Apr-Mar)
- Tenure bounds (join date and exit date exclusions)

---

## 🌐 Hosting on Local Network (LAN Access)

To make the application available to your finance team across a local office network:
```powershell
python -m streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```
Team members can access the app from their web browser using your machine's local IP address:
```
http://<YOUR_LAN_IP>:8501
```

---

## 🛡️ Enterprise Governance & Admin Capabilities

1. **One-Click Backup**: Point-in-time snapshot of `tracker.db` saved with timestamp to `data/backups/`.
2. **Lock Weeks Policy**: Lock submitted weeks older than 30 days to ensure immutable finance audit trails.
3. **One-Click Realistic Demo Data**: Instantly seed or wipe 52 weeks of operational data across 4 teams and 25 employees for presentations or training.
4. **Bulk Data Migrations**: Blank templates and validation engines for importing employee rosters and historical hours in Excel.
