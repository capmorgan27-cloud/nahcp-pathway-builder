import sqlite3
import json
import os

DB_PATH = 'database/nahcp_production.db'

def setup_database():
    """Initializes the NAHCP SQLite database schema with updated roadmap data."""
    # Ensure the database directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Certifications Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS certifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        acronym TEXT,
        category TEXT NOT NULL,
        hours INTEGER NOT NULL
    )
    ''')

    # Clear old data to prevent artifacts from the previous document version
    cursor.execute('DELETE FROM certifications')

    # Seed Data based on Updated NAHCP Sources
    certifications = [
        # STEP 1 & 2: Essentials and Foundations (10 Hours Each)
        ("Medical Terminology Essentials", "MTE", "Essential", 10),
        ("HIPAA & Patient Privacy Essentials", "HPPE", "Essential", 10),
        ("Healthcare CPR/AED & Emergency Response Certification", "HCAERC", "Essential", 10),
        ("Healthcare Safety & Bloodborne Pathogens", "HSBP", "Essential", 10),
        ("Healthcare Workplace Safety & OSHA Essentials", "HWSOE", "Essential", 10),
        ("Hospice & Palliative Care Essentials", "HPCE", "Essential", 10),
        ("Hospice Companion & Volunteer Training Certification", "HCVTC", "Essential", 10),
        
        # STEP 3: Professional Certifications (40 Hours Each)
        ("Certified Healthcare Team Leader", "CHTL", "Professional", 40),
        ("Executive Healthcare Communication & Professional Speaking Certification", "EHCPSC", "Professional", 40),
        ("Certified Healthcare Human Resources Coordinator", "CHHRC", "Professional", 40),
        ("Certified Healthcare Patient Experience Professional", "CHPEP", "Professional", 40),
        ("Certified Healthcare Quality Improvement Professional", "CHQIP", "Professional", 40),
        ("Certified Healthcare Performance Improvement Professional", "CHPIP", "Professional", 40),
        
        # STEP 4: Career Accelerator Boot Camps (App Rules dictating 40 Hours for Pathway)
        ("Assisted Living Facilities Manager State Exam Preparation Boot Camp", "ALFBC", "Boot Camp", 40), #
        ("Executive Leadership Interview Boot Camp", "ELIBC", "Boot Camp", 40), #[cite: 4]
        ("Healthcare Interview Success Boot Camp", "HISBC", "Boot Camp", 40), #[cite: 4]
        ("Healthcare Resume & LinkedIn Boot Camp", "HRLBC", "Boot Camp", 40), #[cite: 4]
        ("Medical Assistant Certification Boot Camp", "MACBC", "Boot Camp", 40), #[cite: 4]
        ("Medical Billing & Coding Certification Boot Camp", "MBCBC", "Boot Camp", 40), #[cite: 4]
        ("NCLEX-PN Boot Camp", "NPNBC", "Boot Camp", 40), #[cite: 4]
        ("NCLEX-RN Boot Camp", "NRNBC", "Boot Camp", 40), #[cite: 4]
        ("New Healthcare Manager Success Boot Camp", "NHMSBC", "Boot Camp", 40), #[cite: 4]
        ("Pharmacy Technician Certification Boot Camp", "PTCBC", "Boot Camp", 40), #[cite: 4]
        
        # STEP 5: Flagship Director Certifications (120 Hours) - Updated List
        ("Certified Dementia/Alzheimer's Director", "CDAD", "Director", 120), #[cite: 4]
        ("Certified Healthcare Community Outreach & Marketing Sales Director", "CHCOMSD", "Director", 120), #[cite: 4]
        ("Certified Healthcare Compliance Officer", "CHCO", "Director", 120), #[cite: 4]
        ("Certified Healthcare Environmental Services Director", "CHESD", "Director", 120), #[cite: 4]
        ("Certified Healthcare Executive Director", "CHED", "Director", 120), #[cite: 4]
        ("Certified Healthcare Finance & Budgeting Director", "CHFB", "Director", 120), #[cite: 4]
        ("Certified Healthcare Information Director", "CHID", "Director", 120), #[cite: 4]
        ("Certified Healthcare Living Enrichment Director", "CHLED", "Director", 120), #[cite: 4]
        ("Certified Healthcare Nutrition & Dining Director", "CHNDD", "Director", 120), #[cite: 4]
        ("Certified Healthcare Project Management Director", "CHPMD", "Director", 120), #[cite: 4]
        ("Certified Hospice Bereavement Director", "CHBD", "Director", 120), #[cite: 4]
        
        # STEP 7: Executive Leadership Fast Track (220 Hours)
        ("Executive Leadership Fast Track™", "ELFT", "Executive", 220) #[cite: 4]
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO certifications (name, acronym, category, hours)
    VALUES (?, ?, ?, ?)
    ''', certifications)

    conn.commit()
    conn.close()
    print("Database seeded successfully with the updated NAHCP structured data.")

if __name__ == "__main__":
    setup_database()