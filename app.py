import os
import streamlit as st

# --- 1. THE SECRET KEY LOGIC ---
# This checks 3 places for your key so it NEVER fails with a 401 error
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
elif "GROQ_API_KEY" in os.environ:
    pass # Already set in local environment
else:
    # If key is missing, show a password box in the sidebar
    st.sidebar.warning("Groq API Key not found in Secrets.")
    user_key = st.sidebar.text_input("Enter Groq API Key to start", type="password")
    if user_key:
        os.environ["GROQ_API_KEY"] = user_key
    else:
        st.info("Please enter your Groq API Key in the sidebar to begin.")
        st.stop() # Stops the app here until a key is entered

# Filler to stop CrewAI from complaining about OpenAI
os.environ["OPENAI_API_KEY"] = "sk-ant-api03-000000000000000000000000000000000000000000"
os.environ["OTEL_SDK_DISABLED"] = "true"

from crewai import Agent, Task, Crew, Process, LLM

# --- 2. THE BRAIN ---
my_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.7
)

st.set_page_config(page_title="AI Coding Coach", layout="wide")
st.title("🎓 Multi-Agent AI Coding Coach")

with st.sidebar:
    st.header("Settings")
    topic = st.text_input("What do you want to learn?", placeholder="e.g. Python Dictionaries")
    level = st.selectbox("Your level", ["Beginner", "Intermediate", "Advanced"])

def run_learning_session(user_topic, user_level):
    tutor = Agent(
        role='Programming Tutor',
        goal=f'Explain {user_topic} to a {user_level} student.',
        backstory="A patient mentor.",
        llm=my_llm,
        verbose=True
    )
    roadmap = Agent(
        role='Roadmap Expert',
        goal=f'Create a study plan for {user_topic}.',
        backstory="A career coach.",
        llm=my_llm,
        verbose=True
    )
    practice = Agent(
        role='Practice Coach',
        goal=f'Create a challenge for {user_topic}.',
        backstory="An examiner.",
        llm=my_llm,
        verbose=True
    )

    t1 = Task(description=f"Explain {user_topic}.", agent=tutor, expected_output="A summary.")
    t2 = Task(description=f"Plan a path.", agent=roadmap, expected_output="A roadmap.")
    t3 = Task(description=f"Create a challenge.", agent=practice, expected_output="A challenge.")

    crew = Crew(
        agents=[tutor, roadmap, practice],
        tasks=[t1, t2, t3],
        process=Process.sequential,
        verbose=True,
        memory=False,
        embedder={
            "provider": "huggingface",
            "config": {"model": "all-MiniLM-L6-v2"}
        }
    )
    return crew.kickoff()

if st.button("Generate Learning Path"):
    with st.spinner("🤖 Agents are collaborating..."):
        try:
            result = run_learning_session(topic, level)
            st.success("Analysis Complete!")
            st.markdown(str(result))
        except Exception as e:
            st.error(f"Error: {e}")
