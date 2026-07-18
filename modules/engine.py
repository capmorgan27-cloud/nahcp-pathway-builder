import sqlite3
import pandas as pd

class PathwayEngine:
    def __init__(self, db_path='database/nahcp_production.db'):
        self.db_path = db_path

    def fetch_courses_by_category(self, category):
        """Retrieves structured data via SQL injection-safe queries."""
        conn = sqlite3.connect(self.db_path)
        query = "SELECT name, hours FROM certifications WHERE category = ?"
        df = pd.read_sql(query, conn, params=(category,))
        conn.close()
        return df

    def build_ideal_pathway(self, target_role, field_interest, experience, weekly_hours):
        """
        Intelligently recommends pathways based on the strict 7-Step framework and tiered prior experience.
        """
        pathway = []
        
        # ---------------------------------------------------------
        # TIERED EXPERIENCE LOGIC
        # ---------------------------------------------------------
        is_beginner = experience in ["No experience", "Less than 2 years"]
        is_advanced = experience in ["5–10 years", "10+ years"]
        
        # Step 1 & 2: Essentials & Foundations (Waived for Intermediate & Advanced)
        if is_beginner:
            pathway.append({"Step": "1", "Type": "Essentials", "Course": "Medical Terminology Essentials", "Hours": 10})
            pathway.append({"Step": "2", "Type": "Foundations", "Course": "HIPAA & Patient Privacy Essentials", "Hours": 10})
        else:
            pathway.append({"Step": "1 & 2", "Type": "Essentials & Foundations", "Course": "Waived (Prior Experience Applied)", "Hours": 0})
        
        # Step 3: Professional Certifications (Waived for Advanced)
        if is_advanced:
             pathway.append({"Step": "3", "Type": "Professional Certification", "Course": "Waived (Advanced Industry Experience Applied)", "Hours": 0})
        else:
            if field_interest == "Human Resources":
                pathway.append({"Step": "3", "Type": "Professional Certification", "Course": "Certified Healthcare Human Resources Coordinator", "Hours": 40}) 
            else:
                pathway.append({"Step": "3", "Type": "Professional Certification", "Course": "Certified Healthcare Team Leader", "Hours": 40}) 
                
            pathway.append({"Step": "3", "Type": "Professional Certification", "Course": "Executive Healthcare Communication", "Hours": 40}) 

        # Step 4: Boot Camps (Required for all levels to prep for targeted transitions)
        if "Executive" in target_role:
            pathway.append({"Step": "4", "Type": "Career Accelerator Boot Camp", "Course": "Executive Leadership Interview Boot Camp", "Hours": 40}) 
        elif "Manager" in target_role:
            pathway.append({"Step": "4", "Type": "Career Accelerator Boot Camp", "Course": "New Healthcare Manager Success Boot Camp", "Hours": 40}) 
        else:
            # Certification Level
            pathway.append({"Step": "4", "Type": "Career Accelerator Boot Camp", "Course": "Healthcare Resume & LinkedIn Boot Camp", "Hours": 40}) 

        # ---------------------------------------------------------
        # HELPER FUNCTION: Add "Estimated Weeks" column
        # ---------------------------------------------------------
        def finalize_pathway(current_pathway):
            for item in current_pathway:
                if item["Hours"] > 0:
                    item["Est. Weeks"] = round(item["Hours"] / weekly_hours, 1)
                else:
                    item["Est. Weeks"] = 0
            return pd.DataFrame(current_pathway)

        # 🛑 STOP HERE FOR LEVEL 1 (Certification Level)
        if "Certification" in target_role:
            return finalize_pathway(pathway)

        # Step 5: Director Level Flagship (120 Hours)
        if field_interest == "Human Resources":
             pathway.append({"Step": "5", "Type": "Flagship Certification", "Course": "Certified Healthcare Executive Director", "Hours": 120}) 
        elif field_interest == "Finance":
             pathway.append({"Step": "5", "Type": "Flagship Certification", "Course": "Certified Healthcare Finance & Budgeting Director", "Hours": 120}) 
        elif field_interest == "Compliance":
             pathway.append({"Step": "5", "Type": "Flagship Certification", "Course": "Certified Healthcare Compliance Officer", "Hours": 120}) 
        else:
             pathway.append({"Step": "5", "Type": "Flagship Certification", "Course": "Certified Healthcare Executive Director", "Hours": 120}) 

        # Step 6: Healthcare Administrator Milestone
        pathway.append({"Step": "6", "Type": "Leadership Milestone", "Course": "Earn Healthcare Administrator Designation", "Hours": 0})

        # 🛑 STOP HERE FOR LEVEL 2 (Manager / Director Level)
        if "Manager" in target_role:
            return finalize_pathway(pathway)

        # Step 7: Executive Leadership Fast Track™ (220 Hours)
        if "Executive" in target_role:
            pathway.append({"Step": "7", "Type": "Executive Track", "Course": "Executive Leadership Fast Track™", "Hours": 220}) 

        return finalize_pathway(pathway)