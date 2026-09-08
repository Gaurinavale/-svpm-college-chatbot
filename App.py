python
import streamlit as st
from groq import Groq
import groq as groq_module

from rag import build_rag, retrieve_documents


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SVPM College Chatbot",
    page_icon="🎓",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .stApp {
        background: linear-gradient(
            135deg,
            #1a1a2e 0%,
            #16213e 50%,
            #0f3460 100%
        );
    }

    .main-header {
        background: linear-gradient(
            90deg,
            #0f3460,
            #533483
        );
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
        background: linear-gradient(
            90deg,
            #0f3460,
            #533483
        );
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


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="main-header">
    <h1>🎓 SVPM College Chatbot</h1>
    <p>SVPM's College of Engineering, Malegaon (Bk), Baramati</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# COLLEGE QUICK INFORMATION
# ============================================================

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


# ============================================================
# QUICK QUESTIONS
# ============================================================

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


# ============================================================
# GROQ CLIENT
# ============================================================

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# INITIALIZE RAG
# ============================================================

@st.cache_resource
def initialize_rag():
    """
    Build and cache the RAG system.

    This loads the college documents,
    creates text chunks,
    generates embeddings,
    and builds the FAISS vector index.
    """

    return build_rag()


# Initialize RAG system
try:

    index, chunks, embedding_model = initialize_rag()

except Exception as e:

    st.error(
        "⚠️ Unable to initialize the RAG system."
    )

    st.error(
        f"Error: {type(e).__name__}: {str(e)}"
    )

    st.stop()


# ============================================================
# RAG + LLM RESPONSE
# ============================================================

def get_response(prompt):

    try:

        # ----------------------------------------------------
        # STEP 1: RETRIEVE RELEVANT INFORMATION
        # ----------------------------------------------------

        results = retrieve_documents(
            query=prompt,
            index=index,
            chunks=chunks,
            model=embedding_model,
            top_k=3
        )


        # ----------------------------------------------------
        # STEP 2: CHECK RETRIEVAL
        # ----------------------------------------------------

        if not results:

            return (
                "I could not find relevant information "
                "in the college knowledge base. "
                "For more details please contact "
                "office@engg.svpm.org.in or call "
                "(02112) 254424.",
                None
            )


        # ----------------------------------------------------
        # STEP 3: CREATE CONTEXT
        # ----------------------------------------------------

        context_parts = []

        for result in results:

            context_parts.append(
                result["text"]
            )

        context = "\n\n".join(
            context_parts
        )


        # ----------------------------------------------------
        # STEP 4: SYSTEM PROMPT
        # ----------------------------------------------------

        system_prompt = """
You are a friendly and helpful AI chatbot
for SVPM's College of Engineering,
Malegaon (Bk), Baramati.

Your task is to answer questions about
the college using ONLY the information
provided in the retrieved context.

IMPORTANT RULES:

1. Use only the retrieved college information.
2. Do not invent facts.
3. Do not make assumptions.
4. If the requested information is not
   available in the context, clearly say
   that the information is not available.
5. When appropriate, provide the official
   college contact information.
6. Keep answers clear, accurate and helpful.
7. Do not mention internal RAG processes
   unless the user asks about the technology.

Official College Contact:

Email:
office@engg.svpm.org.in

Phone:
(02112) 254424

Website:
https://engg.svpm.org.in
"""


        # ----------------------------------------------------
        # STEP 5: CREATE USER PROMPT
        # ----------------------------------------------------

        user_prompt = f"""
Retrieved College Information:

{context}


User Question:

{prompt}


Answer the question using only the
retrieved college information.
"""


        # ----------------------------------------------------
        # STEP 6: CALL GPT-OSS-120B
        # ----------------------------------------------------

        response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": user_prompt
                }

            ]
        )


        # ----------------------------------------------------
        # STEP 7: RETURN RESPONSE
        # ----------------------------------------------------

        reply = response.choices[0].message.content

        return reply, None


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except groq_module.RateLimitError:

        return None, "rate_limit"


    except Exception as e:

        return None, (
            f"{type(e).__name__}: {str(e)}"
        )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="chat-message-user">
                👤 {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="chat-message-bot">
                🎓 {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FUNCTION TO PROCESS USER QUESTION
# ============================================================

def process_question(prompt):

    # Add user message to history

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # Display user question

    st.markdown(
        f"""
        <div class="chat-message-user">
            👤 {prompt}
        </div>
        """,
        unsafe_allow_html=True
    )


    # Generate answer

    with st.spinner("🎓 Searching college information..."):

        reply, error = get_response(prompt)


    # --------------------------------------------------------
    # HANDLE ERRORS
    # --------------------------------------------------------

    if error == "rate_limit":

        st.warning(
            "⚠️ Our chatbot is experiencing "
            "high traffic right now. "
            "Please try again later."
        )

        return


    if error:

        st.error(
            "⚠️ Unable to get a response "
            "from the AI service. "
            "Please try again later."
        )

        return


    # --------------------------------------------------------
    # DISPLAY BOT RESPONSE
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="chat-message-bot">
            🎓 {reply}
        </div>
        """,
        unsafe_allow_html=True
    )


    # Add assistant response to history

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )


# ============================================================
# HANDLE QUICK QUESTION
# ============================================================

if st.session_state.quick_q:

    prompt = st.session_state.quick_q

    st.session_state.quick_q = None

    process_question(prompt)


# ============================================================
# CHAT INPUT
# ============================================================

if prompt := st.chat_input(
    "Ask anything about SVPM College..."
):

    process_question(prompt)


# ============================================================
# FOOTER
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="
    text-align:center;
    color: rgba(255,255,255,0.4);
    font-size: 0.75rem;
">
    🎓 SVPM's College of Engineering |
    Malegaon (Bk), Baramati, Pune |
    Est. 1990
</div>
""", unsafe_allow_html=True)

