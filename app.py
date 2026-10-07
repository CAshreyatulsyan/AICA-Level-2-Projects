import streamlit as st
from datetime import datetime, timedelta
from core.db import init_db, SessionLocal, User, Setting
from core.auth import verify_password, hash_password, ROLE_ADMIN, ROLE_DIRECTOR, ROLE_MANAGER, ROLE_TEAM_LEAD, ROLE_EMPLOYEE
from core.ui_components import apply_custom_css

st.set_page_config(
    page_title="Finance Team Utilization Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database on first run
init_db()
apply_custom_css()

# Session State Initialization
if "user" not in st.session_state:
    st.session_state["user"] = None
if "last_activity" not in st.session_state:
    st.session_state["last_activity"] = datetime.now()

def check_session_timeout():
    """Enforce 60-minute session timeout."""
    if st.session_state["user"]:
        session_duration = datetime.now() - st.session_state.get("last_activity", datetime.now())
        if session_duration > timedelta(minutes=60):
            st.session_state["user"] = None
            st.session_state["last_activity"] = datetime.now()
            st.warning("⚠️ Session expired due to inactivity (60 min timeout). Please log in again.")
            st.stop()
        else:
            st.session_state["last_activity"] = datetime.now()

check_session_timeout()

def login_form():
    st.markdown("""
    <div class="finance-header">
        <h1>📊 Finance Team Utilization Tracker</h1>
        <p>Record-to-Report & Shared Services Operational Capacity Platform</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1.0])

    with col1:
        st.markdown("### 🔐 Secure Login")
        emp_id = st.text_input("Employee ID", placeholder="e.g. EMP001", key="login_emp_id").strip()
        password = st.text_input("Password", type="password", placeholder="Enter password", key="login_pw")
        
        login_btn = st.button("Sign In", type="primary", use_container_width=True)

        if login_btn:
            if not emp_id or not password:
                st.error("Please enter both Employee ID and Password.")
            else:
                session = SessionLocal()
                try:
                    user = session.query(User).filter_by(emp_id=emp_id).first()
                    if user and user.is_active and verify_password(password, user.password_hash):
                        st.session_state["user"] = {
                            "id": user.id,
                            "emp_id": user.emp_id,
                            "name": user.name,
                            "email": user.email,
                            "role": user.role,
                            "location_id": user.location_id,
                            "must_change_pw": user.must_change_pw
                        }
                        st.session_state["last_activity"] = datetime.now()
                        st.success(f"Welcome back, {user.name}!")
                        st.rerun()
                    else:
                        st.error("Invalid Employee ID or Password.")
                finally:
                    session.close()

    with col2:
        st.info("""
        **Quick Evaluation Credentials:**
        
        • **Admin**: `EMP001` / `admin123`  
        • **Director**: `EMP002` / `demo123`  
        • **Team Lead (R2R)**: `EMP003` / `demo123`  
        • **Employee**: `EMP010` / `demo123`  
        
        *All accounts use bcrypt hashing and role-based permissions.*
        """)

def forced_password_change():
    st.warning("🔒 Security Notice: You must change your password on first login.")
    with st.form("change_pw_form"):
        new_pw = st.text_input("New Password", type="password")
        confirm_pw = st.text_input("Confirm New Password", type="password")
        submit_change = st.form_submit_button("Update Password")

        if submit_change:
            if not new_pw or len(new_pw) < 6:
                st.error("Password must be at least 6 characters.")
            elif new_pw != confirm_pw:
                st.error("Passwords do not match.")
            else:
                session = SessionLocal()
                try:
                    user = session.query(User).filter_by(id=st.session_state["user"]["id"]).first()
                    if user:
                        user.password_hash = hash_password(new_pw)
                        user.must_change_pw = False
                        session.commit()
                        st.session_state["user"]["must_change_pw"] = False
                        st.success("Password successfully changed!")
                        st.rerun()
                finally:
                    session.close()

# Main Entry Router
if not st.session_state["user"]:
    login_form()
elif st.session_state["user"].get("must_change_pw"):
    forced_password_change()
else:
    # Authenticated user dashboard landing
    user = st.session_state["user"]
    
    # Sidebar User Profile & Logout
    st.sidebar.markdown(f"**👤 {user['name']}**")
    st.sidebar.caption(f"Role: **{user['role']}** | ID: `{user['emp_id']}`")
    if st.sidebar.button("🚪 Log Out", key="logout_btn", use_container_width=True):
        st.session_state["user"] = None
        st.session_state["last_activity"] = datetime.now()
        st.rerun()

    st.markdown(f"""
    <div class="finance-header">
        <h1>Welcome, {user['name']}</h1>
        <p>Role: {user['role']} &nbsp;|&nbsp; Finance Shared Services &nbsp;|&nbsp; Employee ID: {user['emp_id']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧭 Quick Navigation")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="metric-card">
            <h4>📝 Weekly Entry</h4>
            <p>Log your weekly hours across the 9 finance categories, submit leave, and review your live utilization rate.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Weekly Entry", key="nav_we", use_container_width=True):
            st.switch_page("pages/1_Weekly_Entry.py")

    with c2:
        st.markdown("""
        <div class="metric-card">
            <h4>📜 My History</h4>
            <p>Track your historical submissions, capacity trends, logged hours breakdown, and submission audit trail.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to My History", key="nav_mh", use_container_width=True):
            st.switch_page("pages/2_My_History.py")

    with c3:
        st.markdown("""
        <div class="metric-card">
            <h4>👥 Team View</h4>
            <p>Team Leads & Managers: view team weekly compliance, category load, and member allocations.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Team View", key="nav_tv", use_container_width=True):
            st.switch_page("pages/3_Team_View.py")

    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Management Dashboard</h4>
            <p>Team utilization trends, Employee × Week heatmap, Category matrix, burnout flags, and absence analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Management Dashboard", key="nav_md", use_container_width=True):
            st.switch_page("pages/4_Management_Dashboard.py")

    with c5:
        st.markdown("""
        <div class="metric-card">
            <h4>📈 Director Dashboard</h4>
            <p>Executive review, Close-Cycle WD curves, BAU vs Value-add, capacity forecasting, and PowerPoint export.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Director Dashboard", key="nav_dd", use_container_width=True):
            st.switch_page("pages/5_Director_Dashboard.py")

    with c6:
        st.markdown("""
        <div class="metric-card">
            <h4>📥 Exports & Reports</h4>
            <p>Generate 8-sheet Excel workbooks, download PowerPoint decks, and manage bulk employee / hours imports.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Exports", key="nav_ex", use_container_width=True):
            st.switch_page("pages/6_Exports.py")

    if user["role"] == ROLE_ADMIN:
        st.markdown("---")
        st.markdown("### ⚙️ System Administration")
        col_adm, _ = st.columns([1, 2])
        with col_adm:
            if st.button("🛠️ Open Admin Console", key="nav_adm", type="primary", use_container_width=True):
                st.switch_page("pages/7_Admin.py")
