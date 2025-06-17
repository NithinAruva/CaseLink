# CaseLink
An AI Powered Investigative Intelligence

This project focuses on developing an AI-driven system that integrates video evidence analysis with legal knowledge retrieval to support law enforcement investigations and legal proceedings.

## ✨ Features

- **Automated Video Transcription**: The system transcribes both audio and visual elements in video files. This includes converting speech to text and extracting text from visual cues such as license plates and signboards.
- **A Content Analysis for Key Events**: The system analyzes video content to identify suspicious activities and anomalies like unusual movements or potentially illegal actions. This reduces the manual workload and highlights key moments for investigators.
- **Case File Generation**: Extracted information is used to compile detailed case files. Each file includes suspect activities, relevant observations, and timestamped events, providing investigators with a structured summary.
- **Legal Query System (Agentic RAG)**: Answers context-aware legal questions by linking evidence to Indian and U.S. legal statutes.
- **Intelligent Legal Reasoning**: Uses agent-based retrieval to interpret complex scenarios and recommend applicable legal actions.

## 🖥️ Setup Instructions

1. Install **Python 3.10 or later**.
   
2. Clone the repository:
   ```bash
    git clone https://github.com/NithinAruva/AccidentDetectionSystem.git
    cd AccidentDetectionSystem
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a .env file in your project root directory and add the following lines with your actual API keys:
   ```bash
    GEMINI_API_KEY=your-gemini-api-key-here
    OPENAI_API_KEY=your-openai-api-key-here
   ```
5. Run the application:
   ```bash
   streamlit run app.py
   ```
