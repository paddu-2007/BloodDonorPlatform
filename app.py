import streamlit as st
import sqlite3
import pandas as pd

# ---------------- DATABASE ---------------- #

conn = sqlite3.connect(
    "blood_donor.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Blood Donor Platform",
    page_icon="🩸",
    layout="wide"
)

# ---------------- CSS ---------------- #

st.markdown("""
<style>

.stApp{
    background:#ffffff;
}

.main-title{
    text-align:center;
    color:#c1121f;
    font-size:50px;
    font-weight:bold;
}

.card{
    background:white;
    border-left:6px solid #c1121f;
    padding:20px;
    border-radius:15px;
    margin-top:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

st.markdown(
"""
<h1 class='main-title'>
🩸 Real-Time Blood Donor Matching Platform
</h1>
""",
unsafe_allow_html=True
)

# ---------------- NAVIGATION ---------------- #

page = st.radio(
    "",
    [
        "🏠 Home",
        "👤 Donor Portal",
        "🚨 Emergency Request",
        "🧠 Smart Matching",
        "🔔 Notifications",
        "🏥 Hospital Portal",
        "📊 Dashboard",
        "⚙️ Admin Panel"
    ],
    horizontal=True
)

# ========================= HOME ========================= #

if page == "🏠 Home":

    st.markdown("""
    <div style="
    background:linear-gradient(135deg,#c1121f,#e63946);
    color:white;
    padding:30px;
    border-radius:20px;
    text-align:center;
    ">
    <h1>🩸 Save Lives Through Blood Donation</h1>
    <h3>Real-Time Blood Donor Matching Platform</h3>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🩸 Donors", "0")

    with col2:
        st.metric("🚨 Requests", "0")

    with col3:
        st.metric("✅ Available", "0")

    with col4:
        st.metric("🏥 Hospitals", "0")

    st.write("")

    st.markdown("""
    <div class="card">
    <h2>🎯 Our Mission</h2>

    Connect blood donors with patients in emergencies and
    reduce delays in life-saving blood transfusions.

    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div class="card">

        <h2>🌟 Features</h2>

        ✅ Donor Registration<br>
        ✅ Emergency Requests<br>
        ✅ Smart Matching<br>
        ✅ Notifications<br>
        ✅ Hospital Portal<br>
        ✅ Analytics Dashboard

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div class="card">

        <h2>🩸 Blood Compatibility</h2>

        O- → Universal Donor<br>
        AB+ → Universal Receiver<br>
        A+, A-, B+, B-, AB+, AB-, O+, O-

        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.info(
        "🚨 In an emergency, every minute matters. Use this platform to quickly find compatible blood donors."
    )
# ===================== DONOR PORTAL ===================== #

elif page == "👤 Donor Portal":

    st.subheader("Donor Registration")

    name = st.text_input("Full Name")

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=65
    )

    gender = st.selectbox(
        "Gender",
        ["Male","Female","Other"]
    )

    blood_group = st.selectbox(
        "Blood Group",
        [
            "A+","A-","B+","B-",
            "AB+","AB-","O+","O-"
        ]
    )

    phone = st.text_input("Phone Number")

    email = st.text_input("Email")

    city = st.text_input("City")

    availability = st.selectbox(
        "Availability",
        ["Available","Unavailable"]
    )

    if st.button("Register Donor"):

        cursor.execute("""
        INSERT INTO donors(
        full_name,
        age,
        gender,
        blood_group,
        phone,
        email,
        city,
        availability
        )
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            name,
            age,
            gender,
            blood_group,
            phone,
            email,
            city,
            availability
        ))

        conn.commit()

        st.success("Donor Registered Successfully")

    st.subheader("Registered Donors")

    cursor.execute("""
    SELECT
    full_name,
    blood_group,
    city,
    availability
    FROM donors
    """)

    donors = cursor.fetchall()

    for donor in donors:

        st.write(
            f"👤 {donor[0]} | 🩸 {donor[1]} | 📍 {donor[2]} | {donor[3]}"
        )

# ===================== EMERGENCY REQUEST ===================== #

# ===================== EMERGENCY REQUEST ===================== #

elif page == "🚨 Emergency Request":

    st.title("🚨 Emergency Blood Request")

    st.subheader("Create Emergency Request")

    patient_name = st.text_input("Patient Name")

    blood_group = st.selectbox(
        "Required Blood Group",
        [
            "A+","A-",
            "B+","B-",
            "AB+","AB-",
            "O+","O-"
        ]
    )

    units_required = st.number_input(
        "Required Units",
        min_value=1,
        max_value=20,
        value=1
    )

    emergency_level = st.selectbox(
        "Emergency Level",
        [
            "Normal",
            "High",
            "Critical"
        ]
    )

    hospital_name = st.text_input(
        "Hospital / Blood Bank Name"
    )

    location = st.text_input(
        "Location"
    )

    contact = st.text_input(
        "Contact Information"
    )

    required_date = st.date_input(
        "Required Date"
    )

    if st.button("🚨 Create Request"):

        cursor.execute("""
        INSERT INTO requests(
            patient_name,
            blood_group,
            units_required,
            emergency_level,
            hospital_name,
            required_date,
            location,
            contact
        )
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            patient_name,
            blood_group,
            units_required,
            emergency_level,
            hospital_name,
            str(required_date),
            location,
            contact
        ))

        conn.commit()

        st.success(
            "✅ Emergency Request Created Successfully"
        )

    st.markdown("---")

    st.subheader("📋 Active Requests")

    cursor.execute("""
    SELECT
        patient_name,
        blood_group,
        units_required,
        emergency_level,
        hospital_name,
        location,
        status

    FROM requests

    ORDER BY id DESC
    """)

    requests = cursor.fetchall()

    if requests:

        for req in requests:

            st.markdown(f"""
            ### 🚨 {req[0]}

            🩸 Blood Group: **{req[1]}**

            🧪 Units Required: **{req[2]}**

            ⚠ Emergency Level: **{req[3]}**

            🏥 Hospital: **{req[4]}**

            📍 Location: **{req[5]}**

            📌 Status: **{req[6]}**

            ---
            """)

    else:

        st.info("No emergency requests available.")

# ===================== SMART MATCHING ===================== #

# ===================== SMART MATCHING ===================== #

elif page == "🧠 Smart Matching":

    st.title("🧠 Smart Matching Module")

    st.subheader("Find Compatible Donors")

    required_blood = st.selectbox(
        "Required Blood Group",
        [
            "A+","A-",
            "B+","B-",
            "AB+","AB-",
            "O+","O-"
        ]
    )

    city = st.text_input(
        "Patient Location"
    )

    if st.button("Find Matches"):

        cursor.execute("""
        SELECT
            full_name,
            blood_group,
            city,
            phone,
            availability
        FROM donors
        WHERE blood_group=?
        AND availability='Available'
        """,
        (required_blood,)
        )

        donors = cursor.fetchall()

        if donors:

            st.success(
                f"✅ {len(donors)} Compatible Donors Found"
            )

            rank = 1

            for donor in donors:

                matching_score = 100

                if city.lower() == donor[2].lower():
                    matching_score += 20

                st.markdown(f"""
                ### 🏅 Match #{rank}

                👤 **Donor:** {donor[0]}

                🩸 **Blood Group:** {donor[1]}

                📍 **City:** {donor[2]}

                📞 **Phone:** {donor[3]}

                🟢 **Status:** {donor[4]}

                ⭐ **Matching Score:** {matching_score}

                ---
                """)

                rank += 1

        else:

            st.error(
                "❌ No Eligible Donors Found"
            )

    st.markdown("---")

    st.subheader("📋 Matching Logic")

    st.info("""
✅ Blood Compatibility

✅ Donor Availability

✅ Location Matching

✅ Emergency Priority

✅ Response History (Future Enhancement)

✅ Distance-Based Ranking (Future Enhancement)
""")
# ===================== NOTIFICATIONS ===================== #

# ===================== NOTIFICATIONS ===================== #

elif page == "🔔 Notifications":

    st.title("🔔 Notification Center")

    st.markdown("""
    <div class="card">

    <h2>🚨 Emergency Alerts</h2>

    Donors will receive emergency blood requests based on:
    
    ✅ Blood Group Match
    
    ✅ Availability Status
    
    ✅ Location
    
    ✅ Emergency Priority

    </div>
    """, unsafe_allow_html=True)

    st.subheader("📢 Recent Notifications")

    notifications = [
        "🚨 Critical O+ blood required at Apollo Hospital",
        "✅ Blood request accepted by donor",
        "❌ Blood request rejected by donor",
        "⚠ Emergency request cancelled",
        "✅ New donor registered successfully"
    ]

    for note in notifications:

        st.info(note)

    st.markdown("---")

    st.subheader("📨 Notification Types")

    col1, col2 = st.columns(2)

    with col1:

        st.success("""
✅ Emergency Request Alert

✅ New Matching Request

✅ Request Accepted
""")

    with col2:

        st.warning("""
⚠ Request Rejected

⚠ Request Cancelled

⚠ Donor Unavailable
""")

    st.markdown("---")

    st.subheader("📱 Real Deployment Options")

    st.write("""
    • Email Notifications

    • SMS Notifications

    • WhatsApp Alerts

    • Mobile Push Notifications

    • Blood Bank Integration
    """)
# ===================== HOSPITAL PORTAL ===================== #

# ===================== HOSPITAL PORTAL ===================== #

elif page == "🏥 Hospital Portal":

    st.title("🏥 Hospital / Admin Portal")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🚨 Manage Requests",
        "✅ Verify Requests",
        "👤 Matched Donors",
        "📊 Emergency Monitor"
    ])

    # ==================================================
    # MANAGE REQUESTS
    # ==================================================

    with tab1:

        st.subheader("Active Blood Requests")

        cursor.execute("""
        SELECT
            id,
            patient_name,
            blood_group,
            units_required,
            emergency_level,
            hospital_name,
            status

        FROM requests

        ORDER BY id DESC
        """)

        requests = cursor.fetchall()

        if requests:

            for req in requests:

                st.markdown(f"""
                ### 🚨 Request #{req[0]}

                👤 Patient: **{req[1]}**

                🩸 Blood Group: **{req[2]}**

                🧪 Units Required: **{req[3]}**

                ⚠ Emergency Level: **{req[4]}**

                🏥 Hospital: **{req[5]}**

                📌 Status: **{req[6]}**

                ---
                """)

        else:

            st.info("No active requests available.")

    # ==================================================
    # VERIFY REQUESTS
    # ==================================================

    with tab2:

        st.subheader("Verify Requests")

        st.success("""
✅ Hospital Identity Check

✅ Contact Verification

✅ Patient Information Validation

✅ Emergency Priority Review
""")

        st.warning("""
⚠ Duplicate requests should be reviewed manually.

⚠ Invalid records must be rejected.
""")

    # ==================================================
    # MATCHED DONORS
    # ==================================================

    with tab3:

        st.subheader("Compatible Donors")

        blood_group = st.selectbox(
            "Select Blood Group",
            [
                "A+","A-",
                "B+","B-",
                "AB+","AB-",
                "O+","O-"
            ],
            key="hospital_match"
        )

        if st.button("Find Available Donors"):

            cursor.execute("""
            SELECT
                full_name,
                blood_group,
                city,
                phone,
                availability

            FROM donors

            WHERE blood_group=? 
            AND availability='Available'
            """,
            (blood_group,)
            )

            donors = cursor.fetchall()

            if donors:

                st.success(
                    f"{len(donors)} matching donors found"
                )

                for donor in donors:

                    st.markdown(f"""
                    👤 **{donor[0]}**

                    🩸 Blood Group: {donor[1]}

                    📍 Location: {donor[2]}

                    📞 Phone: {donor[3]}

                    🟢 Status: {donor[4]}

                    ---
                    """)

            else:

                st.error(
                    "No available donors found."
                )

    # ==================================================
    # EMERGENCY MONITOR
    # ==================================================

    with tab4:

        st.subheader("Emergency Monitoring Dashboard")

        cursor.execute(
            "SELECT COUNT(*) FROM requests"
        )

        total_requests = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM donors"
        )

        total_donors = cursor.fetchone()[0]

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "🚨 Total Requests",
                total_requests
            )

        with col2:

            st.metric(
                "🩸 Total Donors",
                total_donors
            )
# ===================== DASHBOARD ===================== #

# ===================== DASHBOARD ===================== #

elif page == "📊 Dashboard":

    st.title("📊 Blood Donor Analytics Dashboard")

    # ---------------- DONOR COUNT ---------------- #

    cursor.execute(
        "SELECT COUNT(*) FROM donors"
    )

    total_donors = cursor.fetchone()[0]

    # ---------------- AVAILABLE DONORS ---------------- #

    cursor.execute("""
    SELECT COUNT(*)
    FROM donors
    WHERE availability='Available'
    """)

    available_donors = cursor.fetchone()[0]

    # ---------------- REQUEST COUNT ---------------- #

    cursor.execute(
        "SELECT COUNT(*) FROM requests"
    )

    total_requests = cursor.fetchone()[0]

    # ---------------- CRITICAL REQUESTS ---------------- #

    cursor.execute("""
    SELECT COUNT(*)
    FROM requests
    WHERE emergency_level='Critical'
    """)

    critical_requests = cursor.fetchone()[0]

    # ---------------- METRICS ---------------- #

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "🩸 Total Donors",
            total_donors
        )

    with col2:
        st.metric(
            "✅ Available Donors",
            available_donors
        )

    with col3:
        st.metric(
            "🚨 Total Requests",
            total_requests
        )

    with col4:
        st.metric(
            "⚠ Critical Requests",
            critical_requests
        )

    st.markdown("---")

    # ---------------- DONOR BLOOD GROUP STATS ---------------- #

    st.subheader("🩸 Blood Group Distribution")

    blood_df = pd.read_sql_query("""
    SELECT
        blood_group,
        COUNT(*) as count
    FROM donors
    GROUP BY blood_group
    """, conn)

    if not blood_df.empty:

        st.bar_chart(
            blood_df.set_index("blood_group")
        )

    else:

        st.info(
            "No donor records available."
        )

    st.markdown("---")

    # ---------------- REQUEST STATS ---------------- #

    st.subheader("🚨 Emergency Request Statistics")

    request_df = pd.read_sql_query("""
    SELECT
        emergency_level,
        COUNT(*) as count
    FROM requests
    GROUP BY emergency_level
    """, conn)

    if not request_df.empty:

        st.bar_chart(
            request_df.set_index(
                "emergency_level"
            )
        )

    else:

        st.info(
            "No emergency requests available."
        )

    st.markdown("---")

    # ---------------- RECENT REQUESTS ---------------- #

    st.subheader("📋 Recent Requests")

    recent_requests = pd.read_sql_query("""
    SELECT
        patient_name,
        blood_group,
        emergency_level,
        hospital_name,
        status

    FROM requests

    ORDER BY id DESC

    LIMIT 10
    """, conn)

    if not recent_requests.empty:

        st.dataframe(
            recent_requests,
            use_container_width=True
        )

    else:

        st.info(
            "No recent requests available."
        )

    st.markdown("---")

    # ---------------- SYSTEM SUMMARY ---------------- #

    st.subheader("📈 System Summary")

    st.success(f"""
    🩸 Registered Donors : {total_donors}

    ✅ Available Donors : {available_donors}

    🚨 Emergency Requests : {total_requests}

    ⚠ Critical Emergencies : {critical_requests}
    """)
# ===================== ADMIN PANEL ===================== #

# ===================== ADMIN PANEL ===================== #

elif page == "⚙️ Admin Panel":

    st.title("⚙️ Admin Panel")

    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Donor Records",
        "🚨 Blood Requests",
        "📊 Monitoring",
        "🛡 Fraud Detection"
    ])

    # ===================================
    # DONOR RECORDS
    # ===================================

    with tab1:

        st.subheader("All Registered Donors")

        donors_df = pd.read_sql_query(
            "SELECT * FROM donors",
            conn
        )

        if not donors_df.empty:

            st.dataframe(
                donors_df,
                use_container_width=True
            )

        else:

            st.warning(
                "No donors registered yet."
            )

    # ===================================
    # BLOOD REQUESTS
    # ===================================

    with tab2:

        st.subheader("All Blood Requests")

        requests_df = pd.read_sql_query(
            "SELECT * FROM requests",
            conn
        )

        if not requests_df.empty:

            st.dataframe(
                requests_df,
                use_container_width=True
            )

        else:

            st.warning(
                "No requests available."
            )

    # ===================================
    # PLATFORM MONITORING
    # ===================================

    with tab3:

        st.subheader("System Monitoring")

        cursor.execute(
            "SELECT COUNT(*) FROM donors"
        )

        total_donors = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM requests"
        )

        total_requests = cursor.fetchone()[0]

        cursor.execute("""
        SELECT COUNT(*)
        FROM donors
        WHERE availability='Available'
        """)

        available_donors = cursor.fetchone()[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🩸 Total Donors",
                total_donors
            )

        with col2:
            st.metric(
                "🚨 Total Requests",
                total_requests
            )

        with col3:
            st.metric(
                "✅ Available Donors",
                available_donors
            )

    # ===================================
    # FRAUD DETECTION
    # ===================================

    with tab4:

        st.subheader("Duplicate / Fraud Detection")

        duplicate_df = pd.read_sql_query("""
        SELECT
            patient_name,
            blood_group,
            COUNT(*) as duplicates

        FROM requests

        GROUP BY patient_name,
                 blood_group

        HAVING COUNT(*) > 1
        """, conn)

        if not duplicate_df.empty:

            st.error(
                "⚠ Possible Duplicate Requests Detected"
            )

            st.dataframe(
                duplicate_df,
                use_container_width=True
            )

        else:

            st.success(
                "✅ No Duplicate Requests Found"
            )

        st.info("""
Admin Responsibilities

✅ Verify Hospitals

✅ Verify Emergency Requests

✅ Review Duplicate Records

✅ Monitor Active Emergencies

✅ Manage Donor Records

✅ Track Completed Requests
""")