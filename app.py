import streamlit as st
import pandas as pd

# Add this line right here, before any other Streamlit commands!
st.set_page_config(layout="wide")

# The rest of your app code goes below...
st.title("Pathway Builder")

# =====================================================================
# 1. Page Configuration & Custom CSS
# =====================================================================
st.markdown("""
    <style>
        /* 1. Your Existing Main App Styles */
        .stApp { background-color: #F8F9FA; }
        .main-header { color: #002D62; font-family: 'Arial', sans-serif; font-weight: 800; }
        div.stButton > button { background-color: #002D62; color: #FFFFFF; border-radius: 5px; }
        div.stButton > button:hover { background-color: #D4AF37; color: #002D62; }
        
        /* 2. NEW: Seamless Navy Sidebar Background */
        [data-testid="stSidebar"] {
            background-color: #002D62 !important;
        }

        /* 3. NEW: Forces all sidebar text to turn white for high contrast */
        [data-testid="stSidebar"] .stText, 
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label {
            color: #FFFFFF !important;
        }

        /* 4. NEW: Tweaks unselected radio buttons so they are visible against the dark background */
        [data-testid="stSidebar"] div[role="radiogroup"] label {
            color: rgba(255, 255, 255, 0.8) !important;
        }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. Initialization
# =====================================================================
engine = PathwayEngine()
if 'admin_action' not in st.session_state:
    st.session_state.admin_action = None

def change_admin_view(view):
    st.session_state.admin_action = view

# =====================================================================
# 3. App Views & Pages
# =====================================================================

def render_questionnaire():
    st.markdown("<h1 class='main-header'>NAHCP Career Path Assessment™</h1>", unsafe_allow_html=True) 
    st.write("Complete this questionnaire to discover your personalized healthcare career pathway, calculate your Career DNA, and unlock your recommended learning journey.")

    with st.form("assessment_form"):
        # --- SECTION 1 ---
        with st.expander("📋 Section 1 - About You", expanded=True):
            age = st.radio("1. What is your age range?", ["Under 18", "18–24", "25–34", "35–44", "45–54", "55+"])
            location = st.selectbox("2. What state do you currently live in?", [
                "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", 
                "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", 
                "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", 
                "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", 
                "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", 
                "New Hampshire", "New Jersey", "New Mexico", "New York", 
                "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", 
                "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
                "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
                "West Virginia", "Wisconsin", "Wyoming"
            ])
            authorized = st.radio("3. Are you legally authorized to work in healthcare in your state?", ["Yes", "No", "Not Sure"])

        # --- SECTION 2 ---
        with st.expander("💼 Section 2 – Healthcare Experience", expanded=True):
            situation = st.selectbox("4. Which best describes your current situation?", [
                "I have never worked in healthcare.", "I am changing careers.", "Caregiver", 
                "Certified Nursing Assistant (CNA)", "Medical Assistant", "Medical Billing & Coding", 
                "Administrative Office Staff", "Human Resources", "Supervisor", "Manager", "Director", "Executive", "Other"
            ])
            years_exp = st.radio("5. How many years have you worked in healthcare?", ["None", "Less than 1 year", "1–3 years", "3–5 years", "5–10 years", "More than 10 years"])
            settings = st.multiselect("6. Which healthcare settings have you worked in? (Check all that apply)", [
                "Hospital", "Assisted Living", "Skilled Nursing", "Memory Care", "Home Health", "Hospice", "Rehabilitation", "Physician Office", "Behavioral Health", "Insurance", "Remote Healthcare", "None"
            ])

        # --- SECTION 3 ---
        with st.expander("🎯 Section 3 - Career Goals", expanded=True):
            primary_goal = st.selectbox("7. What is your primary career goal?", [
                "Get my first healthcare job", "Earn a promotion", "Become a Supervisor", "Become a Manager", 
                "Become a Director", "Become an Executive", "Increase my salary", "Change specialties", 
                "Start my own healthcare business", "Become more competitive in the job market"
            ])
            desired_title = st.selectbox("8. Which healthcare career would you like to have within the next five years?", [
                "Healthcare Administrator", "Executive Director", "Human Resources Director", "Operations Director", 
                "Compliance Manager", "Practice Manager", "Revenue Cycle Manager", "Healthcare Recruiter", 
                "Healthcare Sales & Marketing Manager", "Medical Billing & Coding Professional", "Memory Care Director", 
                "Assisted Living Executive", "Quality Improvement Director", "Healthcare IT Professional", "Education & Training Director"
            ])

        # --- SECTION 4 ---
        with st.expander("⚡ Section 4 – Leadership & Work Style", expanded=True):
            activities = st.multiselect("9. Which activities do you enjoy most?", [
                "Helping people", "Leading teams", "Solving problems", "Teaching others", "Managing projects", 
                "Organizing operations", "Working with technology", "Marketing & Sales", "Working with numbers", "Strategic Planning"
            ])
            strengths = st.multiselect("10. Which skills are your greatest strengths? (Check up to five)", [
                "Leadership", "Communication", "Customer Service", "Organization", "Technology", "Human Resources", "Compliance", "Finance", "Education", "Critical Thinking", "Problem Solving", "Team Building"
            ], max_selections=5)

        # --- SECTION 5 ---
        with st.expander("🎓 Section 5 – Education", expanded=False):
            education = st.radio("11. What is your highest level of education?", ["High School Diploma", "GED", "Certificate", "Associate Degree", "Bachelor's Degree", "Master's Degree", "Doctorate"])
            has_certs = st.radio("12. Do you currently hold any healthcare certifications?", ["Yes", "No"])
            current_certs = st.multiselect("If yes, select all that apply:", ["CPR/BLS", "CNA", "Caregiver", "Medical Assistant", "Medication Technician", "Medical Billing & Coding", "Other"])

        # --- SECTION 6 ---
        with st.expander("⏳ Section 6 – Learning Preferences", expanded=False):
            study_hours = st.radio("13. How many hours per week can you dedicate to studying?", ["2–4 Hours", "5–8 Hours", "8–12 Hours", "More than 12 Hours"])
            format_pref = st.radio("14. Which learning format do you prefer?", ["Self-Paced Online", "Live Online", "Hybrid", "No Preference"])
            timeline = st.radio("15. When would you like to complete your education?", ["As soon as possible", "Within 3 Months", "Within 6 Months", "Within 12 Months", "No Specific Timeline"])

        # --- SECTION 7 & 8 ---
        with st.expander("💰 Section 7 & 8 – Budget & Employer Benefits", expanded=False):
            budget = st.radio("16. What investment are you comfortable making in your education?", ["Under $250", "$250–500", "$500–1,000", "$1,000–2,000", "Over $2,000"])
            reimbursement = st.radio("17. Does your employer offer tuition reimbursement?", ["Yes", "No", "Not Sure"])
            financial_aid = st.radio("18. Would you like information regarding financial assistance (if available)?", ["Yes", "No"])

        # --- SECTION 9 ---
        with st.expander("🧠 Section 9 – Personality & Work Preference", expanded=False):
            personality = st.selectbox("19. Which statement best describes you?", ["Natural Leader", "Team Player", "Detail-Oriented", "Creative Thinker", "Analytical", "Motivator", "Teacher", "Problem Solver"])
            environment = st.selectbox("20. Which work environment do you prefer?", ["Working directly with patients", "Working behind the scenes", "Managing employees", "Working with executives", "Business Operations", "Technology", "A combination of all"])

        submitted = st.form_submit_button("Generate My Personalized Career Pathway")

    if submitted:
        st.markdown("---")
        st.markdown("<h2 class='main-header'>🧬 Your Personalized Career Assessment Results</h2>", unsafe_allow_html=True)
        
        best_match = f"{desired_title}"
        match_percentage = 96 if "Executive" in situation or "Director" in situation else 89
        
        col_match1, col_match2 = st.columns([2, 1])
        with col_match1:
            st.success(f"### **🏆 Your Best Career Match:** {best_match}")
        with col_match2:
            st.metric("Match Score", f"{match_percentage}% Match")

        st.markdown("### 🗺️ Recommended NAHCP Career Pathway")
        
        if "Human Resources" in best_match or "Recruiter" in best_match:
            step1, s1_p = "Healthcare HR Essentials™ (HRE)", 149
            step2, s2_p = "Healthcare Résumé & LinkedIn Boot Camp™ (HRLB)", 99
            step3, s3_p = "Healthcare Human Resources Professional Development Program™ (CHHRP)", 495
            step4, s4_p = "Healthcare Human Resources Leadership Series™ (CHHRD)", 995
        elif "Memory Care" in best_match or "Living" in desired_title:
            step1, s1_p = "Healthcare Leadership Foundations™ (HLF)", 149
            step2, s2_p = "New Healthcare Manager Success Boot Camp™ (NHMS)", 149
            step3, s3_p = "Memory Care Professional Development Program™ (CMCP)", 495
            step4, s4_p = "Dementia & Alzheimer's Leadership Series™ (CDAD)", 995
        elif "Billing" in best_match or "Revenue" in best_match:
            step1, s1_p = "Healthcare Administration Essentials™ (HAE)", 149
            step2, s2_p = "Medical Billing & Coding Exam Prep Boot Camp™ (MBCEP)", 295
            step3, s3_p = "Healthcare Revenue Cycle Basics Professional Development Program™ (CHRCB)", 495
            step4, s4_p = "Healthcare Finance & Budget Leadership Series™ (CHFBD)", 995
        else:
            step1, s1_p = "Healthcare Administration Essentials™ (HAE)", 149
            step2, s2_p = "New Healthcare Manager Success Boot Camp™ (NHMS)", 149
            step3, s3_p = "Healthcare Operations Professional Development Program™ (CHOP)", 495
            step4, s4_p = "Healthcare Administration Leadership Series™ (CHCA)", 995

        st.markdown(f"**Step 1: Foundation Essentials Course**  \n➡️ `{step1}` — Tuition: ${s1_p}")
        st.markdown(f"**Step 2: Healthcare Boot Camp**  \n➡️ `{step2}` — Tuition: ${s2_p}")
        st.markdown(f"**Step 3: Professional Certificate Program**  \n➡️ `{step3}` — Tuition: ${s3_p}")
        st.markdown(f"**Step 4: Executive Leadership Fast Track**  \n➡️ `{step4}` — Tuition: ${s4_p}")

        total_tuition = s1_p + s2_p + s3_p + s4_p
        
        st.markdown("---")
        kpi1, kpi2 = st.columns(2)
        with kpi1:
            st.metric("Estimated Completion Time", "12–18 Weeks", help="Calculated using your custom weekly time investment study profile.")
        with kpi2:
            st.metric("Estimated Tuition Investment", f"${total_tuition:,.2f}", help="Bundled curriculum track savings overview.")

        st.markdown("---")
        st.markdown("### 🧬 Your Career DNA Scores")
        
        dna_scores = {
            "Healthcare Leadership": 65, "Human Resources": 50, "Operations Management": 55,
            "Education & Training": 45, "Compliance": 40, "Healthcare Technology": 40, "Sales & Marketing": 35
        }
        
        if "Leading teams" in activities or "Leadership" in strengths: dna_scores["Healthcare Leadership"] += 25
        if "Human Resources" in situation or "Human Resources" in strengths: dna_scores["Human Resources"] += 41
        if "Organizing operations" in activities or "Managing projects" in activities: dna_scores["Operations Management"] += 34
        if "Teaching others" in activities or "Education" in strengths: dna_scores["Education & Training"] += 38
        if "Compliance" in strengths: dna_scores["Compliance"] += 36
        if "Working with technology" in activities or "Technology" in strengths: dna_scores["Healthcare Technology"] += 32
        if "Marketing & Sales" in activities or "Marketing & Sales" in strengths: dna_scores["Sales & Marketing"] += 33

        for label, score in dna_scores.items():
            final_score = min(score, 99)
            st.write(f"**{label}** ({final_score}%)")
            st.progress(final_score / 100)

        st.markdown("---")
        st.markdown("### 🔍 Top 5 Alternative Career Matches")
        all_matches = ["Healthcare Administrator", "Executive Director", "Operations Director", "Compliance Manager", "Practice Manager", "Revenue Cycle Manager", "Memory Care Director", "Assisted Living Executive"]
        alternatives = [m for m in all_matches if m != best_match][:5]
        for idx, alt in enumerate(alternatives):
            st.write(f"**Match #{idx+1}:** {alt} ({92 - (idx * 3)}% Match)")

        st.markdown("---")
        st.button("🚀 Enroll in Your Personalized Career Pathway Now", use_container_width=True)

def render_pathway_builder():
    st.markdown("<h1 class='main-header'>NAHCP Career Pathway Builder™</h1>", unsafe_allow_html=True)
    
    with st.form("main_pathway_form"):
        target = st.radio("Who do you want to become?", [
            "I want professional certifications to improve my career. (Certification Level)", 
            "I want to become a department manager or director. (Manager / Director Level)", 
            "I want to become an Executive Director, Healthcare Administrator, COO or CEO. (Executive Leadership Level)"
        ])
        
        col1, col2 = st.columns(2)
        with col1:
            field = st.selectbox("Which healthcare field interests you?", ["Administration", "Human Resources", "Finance", "Quality", "Compliance", "Executive Leadership", "Hospice", "Medical Billing"])
            setting = st.selectbox("Which setting interests you?", ["Hospital", "Assisted Living", "Memory Care", "Skilled Nursing", "Hospice", "Medical Office"])
        with col2:
            experience = st.selectbox("Do you already work in healthcare?", ["No experience", "Less than 2 years", "2–5 years", "5–10 years", "10+ years"])
            study_time = st.selectbox("How much time can you study each week?", ["2 hours", "5 hours", "10 hours", "15 hours", "20+ hours", "40 hours"])
            
        submitted = st.form_submit_button("Build My Career Pathway")

    if submitted:
        weekly_hours = int(study_time.split(" ")[0].replace("+", ""))
        df_pathway = engine.build_ideal_pathway(target, field, experience, weekly_hours)
        
        def get_avg_price(hours):
            if hours <= 10: return 149
            elif hours <= 40: return 395 
            elif hours <= 120: return 995 
            elif hours >= 220: return 1495 
            return 0
            
        df_pathway['Est. Cost'] = df_pathway['Hours'].apply(get_avg_price)
        
        if "Executive Leadership Level" in target:
            salary_range = "$130,000 - $250,000+"
        elif "Manager / Director Level" in target:
            salary_range = "$85,000 - $125,000"
        else:
            salary_range = "$55,000 - $75,000"

        total_hours = df_pathway['Hours'].sum()
        total_weeks = round(total_hours / weekly_hours, 1)
        actual_courses = len(df_pathway[df_pathway['Hours'] > 0])
        total_cost = df_pathway['Est. Cost'].sum()
        
        kpi1, kpi2, kpi3, kpi_cost, kpi4, spacer, kpi5 = st.columns([1.2, 1.2, 1.2, 1.5, 2.5, 0.4, 3]) 
        
        kpi1.metric("Total Hours", f"{total_hours} Hrs")
        kpi2.metric("Total Weeks", f"{total_weeks} Wks")
        kpi3.metric("Courses", actual_courses)
        kpi_cost.metric("Total Tuition", f"${total_cost:,.2f}")
        
        if field == "Administration":
            clean_field = "Administrative"
        else:
            clean_field = field

        if "Certification" in target:
            destination_title = f"{clean_field} Specialist"
        elif "Manager" in target:
            destination_title = f"{clean_field} Manager"
        else:
            destination_title = "Executive Leadership Level"

        kpi4.metric("Destination", destination_title)
        
        kpi5.markdown(
            f"<div style='font-size: 14px; color: #555; margin-bottom: 0px;'>Estimated Salary</div>"
            f"<div style='font-size: 2.25rem; color: #31333F; margin-top: 0px;'>{salary_range}</div>", 
            unsafe_allow_html=True
        )
        
        st.markdown("""
            <style>
                table th { text-align: left !important; }
                table td { text-align: left !important; }
            </style>
        """, unsafe_allow_html=True)
        
        df_display = df_pathway.copy()
        df_display["Est. Weeks"] = df_display["Est. Weeks"].apply(lambda x: f"{x:.1f}")
        df_display["Est. Cost"] = df_display["Est. Cost"].apply(lambda x: f"${x:,.2f}")
        
        total_row = {col: "" for col in df_display.columns}
        total_row["Est. Weeks"] = "TOTAL"
        total_row["Est. Cost"] = f"${total_cost:,.2f}"
        
        df_display.loc[len(df_display)] = total_row
        st.table(df_display.style.hide(axis="index"))
        st.success("Pathway generated successfully!")

def render_dashboard():
    st.markdown("<h1 class='main-header'>Student Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #555;'><em>Use these controls to simulate student progress:</em></p>", unsafe_allow_html=True)
    
    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        total_courses = st.number_input("Total Courses in Pathway", min_value=1, value=8)
        completed_courses = st.slider("Courses Completed", min_value=0, max_value=total_courses, value=2)
    with sim_col2:
        total_hours = st.number_input("Total Hours Required", min_value=10, value=480, step=10)
        completed_hours = st.slider("Hours Completed", min_value=0, max_value=total_hours, value=50)

    st.markdown("---")

    remaining_courses = total_courses - completed_courses
    progress_percentage = completed_hours / total_hours

    col1, col2, col3 = st.columns(3)
    col1.metric("Completed", str(completed_courses))
    col2.metric("Remaining", str(remaining_courses))
    col3.metric("Current Hours", f"{completed_hours} / {total_hours}")
    
    st.progress(progress_percentage)
    
    st.subheader("Achievements")
    if completed_courses >= 1:
        st.success("🏆 Badge Earned: First Course Completed!")
    if progress_percentage >= 0.5 and progress_percentage < 1.0:
        st.info("🔥 Halfway There! Keep up the great work!")
    if completed_courses == total_courses and completed_hours == total_hours:
        st.balloons()
        st.success("🎓 Pathway Complete! Congratulations!")

def render_admin_panel():
    st.markdown("<h1 class='main-header'>NAHCP Admin Panel</h1>", unsafe_allow_html=True)
    
    if st.session_state.admin_action is None:
        st.write("Select an action below to manage your catalog and pathways.")
        col1, col2 = st.columns(2)
        with col1:
            st.button("➕ Add New Certification", on_click=change_admin_view, args=("adding",), use_container_width=True)
        with col2:
            st.button("📝 Edit Pathways", on_click=change_admin_view, args=("editing",), use_container_width=True)
            
    elif st.session_state.admin_action == "adding":
        st.button("⬅️ Back to Panel", on_click=change_admin_view, args=(None,), key="back_add")
        st.subheader("Add New Certification")
        
        with st.form("new_cert_form"):
            cert_name = st.text_input("Program Name", placeholder="e.g., Certified Healthcare Executive Director™")
            category = st.selectbox("Category", ["10-Hour Essentials", "40-Hour Professional", "120-Hour Flagship", "Boot Camp", "220-Hour Fast Track"])
            hours = st.number_input("Total Hours", min_value=10, step=10)
            price = st.number_input("Suggested Price ($)", min_value=0, step=50)
            
            if st.form_submit_button("Save to Master Inventory"):
                st.success(f"Successfully added **{cert_name}** to your catalog! (Simulation)")

    elif st.session_state.admin_action == "editing":
        st.button("⬅️ Back to Panel", on_click=change_admin_view, args=(None,), key="back_edit")
        st.subheader("Edit Pathways")
        st.info("The visual pathway editor will go here.")

# =====================================================================
# 4. Main App Routing Engine
# =====================================================================
def main():
    # Centers the transparent logo in the sidebar
    col1, col2, col3 = st.sidebar.columns([1, 4, 1])
    with col2:
        st.image("logo.png", use_container_width=True)
        
    st.sidebar.title("Navigation")
    
    # ADDED "Career Path Assessment" to the list so users can open it!
    app_mode = st.sidebar.radio("Go to", [
        "Career Path Assessment",
        "Career Pathway Builder", 
        "Student Dashboard", 
        "Admin Panel"
    ])

    if app_mode == "Career Path Assessment":
        render_questionnaire()
    elif app_mode == "Career Pathway Builder":
        render_pathway_builder()
    elif app_mode == "Student Dashboard":
        render_dashboard()
    elif app_mode == "Admin Panel":
        render_admin_panel()

if __name__ == "__main__":
    main()
