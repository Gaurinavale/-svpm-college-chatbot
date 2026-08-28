import streamlit as st
from groq import Groq
import groq as groq_module

# Page config
st.set_page_config(
    page_title="SVPM College Chatbot",
    page_icon="🎓",
    layout="centered"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }

    .main-header {
        background: linear-gradient(90deg, #0f3460, #533483);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .main-header h1 {
        color: white;
        font-size: 2rem;
        margin: 0;
    }

    .main-header p {
        color: #a0c4ff;
        margin: 5px 0 0 0;
        font-size: 1rem;
    }

    .info-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 10px 15px;
        margin: 5px 0;
        color: white;
        font-size: 0.85rem;
    }

    .chat-message-user {
        background: linear-gradient(90deg, #0f3460, #533483);
        color: white;
        padding: 12px 16px;
        border-radius: 15px 15px 0px 15px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }

    .chat-message-bot {
        background: rgba(255,255,255,0.08);
        color: white;
        padding: 12px 16px;
        border-radius: 15px 15px 15px 0px;
        margin: 8px 0;
        max-width: 85%;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }

    .stButton > button {
        background: rgba(255,255,255,0.08);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 5px 12px;
        font-size: 0.8rem;
        transition: all 0.3s;
        width: 100%;
    }

    .stButton > button:hover {
        background: rgba(83, 52, 131, 0.5);
        border-color: #533483;
        transform: translateY(-1px);
    }

    .stChatInput input {
        background: rgba(255,255,255,0.08) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 25px !important;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


# College FAQ - Complete Information
faq_text = """
=== GENERAL INFORMATION ===
Full Name: SVPM's College of Engineering, Malegaon (Bk), Baramati, Pune.
Institute Code: 6275
Established: 1990. First B.E. batch graduated in 1994. 35+ years of excellence.
Campus Size: 20 hectares with RCC structures for education, labs, hostels, sports, cafeteria.
Address: Malegaon (Bk.), Baramati, Pune, Maharashtra, India. Pin: 413115.
Phone: (02112) 254424
Fax: (02112) 254424
Email: office@engg.svpm.org.in
Website: https://engg.svpm.org.in
Awards: India's Best Engineering Institute Award received.

=== MANAGEMENT ===
President: Hon. Shri. Sharadchandraji Pawar, Ex. Minister for Agriculture, Govt. of India and Ex. Chief Minister of Maharashtra.
Managing Body: Shivnagar Vidya Prasarak Mandal (SVPM)
Principal: Prof. Dr. Shailendrakumar M. Mukane (M. Tech., Ph.D.)
Principal Email: principal@engg.svpm.org.in
Governing Body: https://engg.svpm.org.in/management-trustees
College Development Committee: https://engg.svpm.org.in/college-development-committee

=== VISION, MISSION & COMMITMENT ===
Vision: To be nationally recognized as a centre of excellence in the field of technical education.
Mission: To provide transformative education through integration of academic excellence, research, skills and values.
Commitment: To contribute to the national goal of upliftment of the society through Science and Technology.

=== APPROVALS & AFFILIATIONS ===
Affiliated to: Savitribai Phule Pune University (SPPU)
Approved by: AICTE, NAAC, DTE, Government of Maharashtra
NAAC: Accredited
NIRF: https://engg.svpm.org.in/nirf

=== DEPARTMENTS ===
1. First Year Engineering
2. Mechanical Engineering
3. Electronics and Telecommunication Engineering
4. Computer Engineering
5. Information Technology - HOD: Prof. Dr. J. S. Gawade
6. Civil Engineering
7. Electrical Engineering
8. Mechatronics Engineering
9. Artificial Intelligence and Machine Learning (AI & ML) - Newly launched with modern curriculum

Postgraduate (M.E.) courses:
- Electronics & Telecommunication Engineering (Digital Systems)
- Mechanical Engineering (Design Engineering)

=== IT DEPARTMENT DETAILS ===
HOD: Prof. Dr. J. S. Gawade
Vision: To recognize as a center of excellence in the field of Information Technology.
Mission: Develop students in application oriented knowledge along with nurturing them in research and employability skills.
Faculty Profile: https://engg.svpm.org.in/information-faculty-profile
Laboratory Details: https://engg.svpm.org.in/it-laboratory-details
Syllabus: https://engg.svpm.org.in/it-syllabus
Timetable: https://engg.svpm.org.in/it-time-table
Academic Calendar: https://engg.svpm.org.in/it-academic-calendar
Result Analysis: https://engg.svpm.org.in/it-result-analysis
Projects: https://engg.svpm.org.in/it-projects
MOUs: https://engg.svpm.org.in/it-mou
Achievements: https://engg.svpm.org.in/it-departmental-achievement

=== ADMISSIONS ===
Courses: B.E. in Mechanical, Electronics & Telecomm, Computer, IT, Civil, Electrical, Mechatronics, AI & ML.
Process: CAP (Centralized Admission Process) by DTE Maharashtra + Institute Level admissions.
Eligibility: https://engg.svpm.org.in/eligibility
Documents Required: https://engg.svpm.org.in/documents-required
Fee Structure: https://engg.svpm.org.in/fra-fee-structure
Fee Structure 2025-26 English: https://engg.svpm.org.in/files/2025-26/fee-english.pdf
Fee Structure 2025-26 Marathi: https://engg.svpm.org.in/files/2025-26/fee-marathi1.pdf
FE Admission Contacts:
- Prof. J. Y. Pawar: 8600709174
- Prof. R. A. Jadhav: 9423250477
- Prof. V. A. Choughule: 9762279779
- Institute Level: Prof. Mrs. Mokashi S. S.: 9657646267
Existing Students: https://engg.svpm.org.in/existing-students-admission
Admission Enquiry 2025-26: https://engg.svpm.org.in/admission-enquiry
Information Brochure: https://engg.svpm.org.in/files/SVPM-COE-4.pdf
Mandatory Disclosure: https://engg.svpm.org.in/files/Mandatory-Disclosure-2023-24.pdf

=== FACILITIES ===
Library: Well-equipped library with physical books and e-Library. https://engg.svpm.org.in/library
e-Library: https://engg.svpm.org.in/e-library
Auditorium: Available for events and seminars. https://engg.svpm.org.in/auditorium
Boys Hostel: Available on campus. https://engg.svpm.org.in/boys-hostel-facilities
Girls Hostel: Available on campus. https://engg.svpm.org.in/girls-hostel-facilities
Cafeteria: Available on campus. https://engg.svpm.org.in/cafeteria
Gymnasium: Available on campus. https://engg.svpm.org.in/gymnasium
Sports: Dedicated sports area with various activities. https://engg.svpm.org.in/sports
Coursera Access: https://www.coursera.org/programs/svpms-college-of-engineering-malegaon-bk-baramat-on-coursera-oq9ws
Virtual Labs: https://www.vlab.co.in
Student ERP: https://mysvpm.edupluscampus.com/
Staff ERP: https://adminsvpm.edupluscampus.com/login/erphome
Capgemini Digital Lab: Inaugurated on campus.

=== PLACEMENTS ===
Total Placed This Year: 175
Total Offers This Year: 185
Highest Package: 12.3 LPA
Average Package: 4.0 LPA
Total Placements in 4 Years: 1300+
Training & Placement Cell: https://engg.svpm.org.in/training-cell
Placement Records: https://engg.svpm.org.in/placed-records
Placement Events: https://engg.svpm.org.in/placement-events
Recruiters List: https://engg.svpm.org.in/our-recruiters
Top Recruiters: Capgemini, TCS, Infosys, Cognizant, Bosch, Adani Cement, Mastek, Indovance, KPIT, Persistent Systems, Reliance Jio, Sahyadri Software, R Square Soft Technologies, QSpiders, Zensoft, Kirloskar, Everest Ltd, Walchandnagar Industries.
Training provided: Aptitude Training, Technical Training, Personality Development, Campus Drives.

=== SCHOLARSHIPS ===
1. Sharadchandra Pawar Scholarship (applications invited)
2. FORSTU Scholarships
3. Government fee waiver for Girl Students (GR issued)
4. AICTE Scholarship/Fellowship Schemes
5. VidyaLaxmi Portal for education loans: https://www.vidyalakshmi.co.in/
Scholarship page: https://engg.svpm.org.in/scholarship
Earn and Learn Scheme: https://engg.svpm.org.in/earn-and-learn

=== ACADEMICS ===
Academic Calendar: https://engg.svpm.org.in/institute-academic-calendar
Code of Conduct: https://engg.svpm.org.in/code-of-conduct
Administrative Committee: https://engg.svpm.org.in/administrative-committee

=== RESEARCH & DEVELOPMENT ===
R&D Cell: https://engg.svpm.org.in/about-research-development-cell
Research Grant: Government of India granted Research Fund to Dr. Devendra Agarwal.
Patents: Dr. D. P. Agrawal received Patent Grant. https://engg.svpm.org.in/patents
Publications: https://engg.svpm.org.in/publications
International Conference: https://engg.svpm.org.in/international-conference
Funding: https://engg.svpm.org.in/funding
MoUs: Bhasha Academy (German Language Center), Capgemini Digital Lab.

=== COMMITTEES ===
Anti-Ragging Committee: https://engg.svpm.org.in/anti-ragging
SC/ST Committee: https://engg.svpm.org.in/scst-committee
Grievance Redressal Cell: https://engg.svpm.org.in/grievance-redressal-cell
Internal Complaints Committee (ICC): https://engg.svpm.org.in/internal-complaints-committee
Equal Opportunity Cell: https://engg.svpm.org.in/equal-opportunity-cell
Divyang Cell: https://engg.svpm.org.in/divyang-cell
Student Council: https://engg.svpm.org.in/student-council
All Committees: https://engg.svpm.org.in/committees
NSS Activity: https://engg.svpm.org.in/nss-activity
Student Welfare: https://engg.svpm.org.in/student-welfare

=== EVENTS & FESTIVALS ===
CRETECHNOVA: Annual technical festival (CRETECHNOVA-2K26 upcoming)
CHAITANYA: Annual cultural festival
RETRACE: Annual Alumni Meet
AAVISHKAR: Research competition (Success in AAVISHKAR 2024-25)
NSS Blood Donation Camp: Organized regularly
No Vehicles Day: Organized on campus
Indian Air Force IPEV Road Drive: Organized on campus
ATAL FDP Programs: On AI & ML, Next Generation Communication, Semiconductor Technology etc.
National Conference NCETET: https://engg.svpm.org.in/ncetet2023

=== HOW TO REACH ===
By Train:
- Baramati Railway Station: 9 KM
- Daund: 50 KM
- Pune: 100 KM
- Mumbai: 260 KM
By Air:
- Pune Airport: 100 KM
- Mumbai Airport: 260 KM
By Bus: State Transport buses from Pune-Swargate every 30 minutes. Nearest bus station: Baramati.
Google Maps: Search "SVPM College of Engineering Malegaon Baramati"

=== IMPORTANT LINKS ===
Alumni Registration: https://engg.svpm.org.in/alumni
Career/Jobs at College: https://engg.svpm.org.in/career
Gallery: https://engg.svpm.org.in/gallery
IQAC: https://engg.svpm.org.in/AQAR
NAAC Accreditation: https://engg.svpm.org.in/naac-accreditation
AICTE Approval Letters: https://engg.svpm.org.in/aicte-approval-letters
AICTE Website: http://www.aicte-india.org
SPPU Website: http://unipune.ac.in
DTE Website: http://www.dte.org.in
"""


# Header
st.markdown("""
<div class="main-header">
    <h1>🎓 SVPM College Chatbot</h1>
    <p>SVPM's College of Engineering, Malegaon (Bk), Baramati</p>
</div>
""", unsafe_allow_html=True)


# College quick info cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="info-card">📞 (02112) 254424</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div class="info-card">📧 office@engg.svpm.org.in</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        '<div class="info-card">🏛️ Est. 1990 | Code: 6275</div>',
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)


# Quick question buttons
st.markdown("**💡 Quick Questions:**")

quick_questions = {
    "👨‍💼 Principal": "Who is the principal?",
    "🏢 Departments": "What departments are available?",
    "💰 Placements": "What is the placement record?",
    "🎓 Admission": "How to take admission?",
}


if "quick_q" not in st.session_state:
    st.session_state.quick_q = None


cols = st.columns(4)

for i, (label, question) in enumerate(quick_questions.items()):
    with cols[i]:
        if st.button(label):
            st.session_state.quick_q = question


# Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Show chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(
            f'<div class="chat-message-user">👤 {message["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-message-bot">🎓 {message["content"]}</div>',
            unsafe_allow_html=True
        )


# System prompt
system_prompt = f"""
You are a friendly and helpful chatbot for SVPM's College of Engineering, Malegaon (Bk), Baramati.

Answer questions based ONLY on the college information provided below.

Give clear, helpful and complete answers.

If the answer is not in the information, say:
"For more details please contact office@engg.svpm.org.in or call (02112) 254424 or visit https://engg.svpm.org.in"

COLLEGE INFORMATION:

{faq_text}
"""


# Helper function to call Groq
def get_response(prompt):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content, None

    except groq_module.RateLimitError:
        return None, "rate_limit"

    except Exception as e:
        return None, f"{type(e).__name__}: {str(e)}"


# Handle a quick-question button click
if st.session_state.quick_q:
    prompt = st.session_state.quick_q
    st.session_state.quick_q = None

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    st.markdown(
        f'<div class="chat-message-user">👤 {prompt}</div>',
        unsafe_allow_html=True
    )

    with st.spinner("🎓 Thinking..."):
        reply, error = get_response(prompt)

    if error == "rate_limit":
        st.warning(
            "⚠️ Our chatbot is experiencing high traffic right now. "
            "Please try again later."
        )
    elif error:
        st.error(f"⚠️ AI Error: {error}")
    else:
        st.markdown(
            f'<div class="chat-message-bot">🎓 {reply}</div>',
            unsafe_allow_html=True
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )


# Chat input
if prompt := st.chat_input("Ask anything about SVPM College..."):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    st.markdown(
        f'<div class="chat-message-user">👤 {prompt}</div>',
        unsafe_allow_html=True
    )

    with st.spinner("🎓 Thinking..."):
        reply, error = get_response(prompt)

    if error == "rate_limit":
        st.warning(
            "⚠️ Our chatbot is experiencing high traffic right now. "
            "Please try again later."
        )
    elif error:
        st.error("⚠️ Unable to get a response from the AI service. Please try again later.")
    else:
        st.markdown(
            f'<div class="chat-message-bot">🎓 {reply}</div>',
            unsafe_allow_html=True
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )


# Footer
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; color: rgba(255,255,255,0.4); font-size: 0.75rem;">
    🎓 SVPM's College of Engineering | Malegaon (Bk), Baramati, Pune | Est. 1990
</div>
""", unsafe_allow_html=True)
