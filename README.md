# BuddhiX — Working AI Learning Agent Prototype

This ZIP contains a local Streamlit app with ASI:One API integration, structured Analysis Mode, AI-generated MCQ quizzes with local scoring, Learning Kit, Study Planner, selectable-text PDF extraction for Notes Q&A, and SQLite quiz progress.

## Honest implementation status
This is a single-app AI agent prototype, **not yet a deployed distributed Fetch.ai uAgents network**. The Agent Blueprint page separates implemented app features from planned independent network agents.

## Setup on Windows
1. Extract this ZIP to a normal folder.
2. Copy `.env.example` to `.env`.
3. Open `.env` in VS Code and set `ASI_ONE_API_KEY=your_actual_key`. Never share this key or upload `.env`.
4. Double-click `run_windows.bat`. If the terminal pauses before launching, press a key and run `streamlit run app.py` in the activated terminal.
5. Open the local URL shown, usually http://localhost:8501.

ASI:One's OpenAI-compatible endpoint is `https://api.asi1.ai/v1/chat/completions`. API use may consume account credits or be billed. Check your dashboard.

## Python
If Python 3.15 causes dependency errors, use Python 3.12 or 3.13 in a separate environment; don't uninstall other versions automatically.

## 90-second demo
1. Ask a question in Analysis Mode.
2. Generate a 3-question quiz, answer it, submit, and show explanations.
3. Open My Progress to show the recorded score.
4. Generate a study plan.
5. Open Agent Blueprint and explain that distributed uAgents are the next milestone, not yet implemented.

Limitations: scanned PDF OCR, cloud sync, voice tutor, web search and independent distributed uAgents are not included in this version.
