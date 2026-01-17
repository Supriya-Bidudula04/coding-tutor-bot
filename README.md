# coding-tutor-bot
# 🎓 AI Multi-Agent Coding Coach

### 🚀 Problem Statement
College students often struggle to learn programming effectively because they lack personalized guidance, structured learning paths, and instant feedback on their practice exercises. 

### 💡 The Solution
This application uses a **Multi-Agent Architecture** powered by **Groq (Llama 3.3)** and **CrewAI** to provide a 3-in-1 learning experience:
1. **Personalized Tutoring:** Explains concepts based on the user's skill level.
2. **Dynamic Roadmaps:** Generates a 4-week industry-aligned study plan.
3. **Smart Evaluation:** Provides custom coding challenges and grading criteria.

---

## 🧠 Agent Architecture & Roles

- **🧠 Agent 1: Programming Tutor Agent**
  - **Role:** Explains programming concepts (Python/Java).
  - **Goal:** Clear doubts and provide simple examples adapted to the user's level.
- **📅 Agent 2: Learning Roadmap Agent**
  - **Role:** Career & Study Coach.
  - **Goal:** Align learning with industry-relevant skills and suggest progression paths.
- **📝 Agent 3: Practice & Evaluation Agent**
  - **Role:** Technical Examiner.
  - **Goal:** Generate exercises and provide constructive feedback on responses.

---

## 🛠️ Tech Stack
- **LLM:** Groq (Llama-3.3-70b-versatile)
- **Framework:** CrewAI (Agent Orchestration)
- **UI:** Streamlit
- **Embeddings:** HuggingFace (Local)

---

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/your-repo-name.git
   cd your-repo-name
