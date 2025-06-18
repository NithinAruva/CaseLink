# CaseLink

This project focuses on developing an AI-driven system that integrates video evidence analysis with legal knowledge retrieval to support law enforcement investigations and legal proceedings.

## ✨ Features

- **Automated Video Transcription**: The system transcribes both audio and visual elements in CCTV footage. This includes converting speech to text and extracting text from visual cues such as license plates and signboards.
- **A Content Analysis for Key Events**: The system analyzes video content to identify suspicious activities and anomalies like unusual movements or potentially illegal actions. This reduces the manual workload and highlights key moments for investigators.
- **Case File Generation**: Extracted information is used to compile detailed case files. Each file includes suspect activities, relevant observations, and timestamped events, providing investigators with a structured summary.
- **Legal Query System (Agentic RAG)**: Answers context-aware legal questions by linking evidence to Indian and U.S. legal statutes.
- **Intelligent Legal Reasoning**: Uses agent-based retrieval to interpret complex scenarios and recommend applicable legal actions.

## 🖥️ Setup Instructions

1. Install **Python 3.10 or later**.
   
2. Clone the repository:
   ```bash
    git clone https://github.com/NithinAruva/CaseLink.git
    cd CaseLink
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

## ⚙️ Output

![Image](https://github.com/user-attachments/assets/3a32b717-8c12-40c7-affa-a278738fe77e)

![Image](https://github.com/user-attachments/assets/5c0120b3-a561-4c52-bdbc-0e6f56aca736)

![Image](https://github.com/user-attachments/assets/6f0cb8ef-a527-4a23-97b3-c28c65c7ccdf)

![Image](https://github.com/user-attachments/assets/c2f98a2f-9da1-4506-9251-837456d66726)

![Image](https://github.com/user-attachments/assets/9a6be3dd-ea78-4c33-8797-bb362023afd2)


