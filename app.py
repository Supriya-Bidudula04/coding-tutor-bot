import os
import streamlit as st

# 1. SET THE GROQ KEY DIRECTLY IN THE ENVIRONMENT
# Replace with your actual gsk_... key
os.environ["GROQ_API_KEY"] = "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"

# 2. THE SECRET SAUCE: Give it a fake OpenAI key that LOOKS real 
# but tell the system to NEVER use it.
os.environ["OPENAI_API_KEY"] = "sk-ant-api03-000000000000000000000000000000000000000000"

# Stop telemetry errors
os.environ["OTEL_SDK_DISABLED"] = "true"

from crewai import Agent, Task, Crew, Process, LLM

# 3. Define the LLM once using the 'groq/' prefix
# This is the most modern way to use Groq with CrewAI
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
    # Every Agent MUST have the 'llm' parameter
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

    t1 = Task(description=f"Explain {user_topic}.", agent=tutor, expected_output="An explanation.")
    t2 = Task(description=f"Plan a path.", agent=roadmap, expected_output="A roadmap.")
    t3 = Task(description=f"Create a challenge.", agent=practice, expected_output="A challenge.")

    # 4. OVERRIDE THE CREW DEFAULTS
    # We explicitly set the embedder to 'huggingface' so it doesn't call OpenAI
    crew = Crew(
        agents=[tutor, roadmap, practice],
        tasks=[t1, t2, t3],
        process=Process.sequential,
        verbose=True,
        memory=False, # Disable memory to be safe
        embedder={
            "provider": "huggingface",
            "config": {
                "model": "all-MiniLM-L6-v2"
            }
        }
    )
    
    return crew.kickoff()

if st.button("Generate Learning Path"):
    if not topic:
        st.error("Please enter a topic in the sidebar!")
    else:
        with st.spinner("🤖 Agents are collaborating (this takes ~30 seconds)..."):
            try:
                result = run_learning_session(topic, level)
                st.success("Analysis Complete!")
                st.markdown(str(result))
            except Exception as e:
                st.error(f"Error: {e}")