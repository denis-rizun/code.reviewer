# 🤖 Code.Reviewer — AI-Powered OSS Repo Auditor

This is an **AI-driven auditor** for open-source GitHub repositories.  
Built with **Go**, **Python** and a modular microservice architecture designed for high-throughput environments.

> ⚠️ **Project is currently in active development.** Features and architecture may evolve rapidly.

---

## 🚀 Project Goal

To create an intelligent assistant that audits public GitHub repositories and evaluates:  
- 📚 Documentation completeness
- 🧪 Test coverage
- ⚙️ CI/CD configurations
- 🧠 Code structure and complexity
- 🔍 Repository activity & contributor health
- 🔧 Improvement recommendations (TODOs)

---

## 📦 Architecture (detailed flow)

User  
- Interface Layer (Telegram Bot / Web UI)  
- `Go` API Gateway  
    - Validates repo URL  
    - Publishes task to Kafka topic  
- `Kafka` Broker  
    - Delivers tasks to processing workers  
- `Python` Analyzer  
    - Scans repo  
    - Runs static checks (AST, complexity, linters)  
    - Applies AI models (e.g., doc quality, commit-history health)  
    - Summarizes result as JSON & Markdown  
- User receives structured audit report  

---

## 📚 Example usage (planned, in case with Telegram Bot)


👤 User: /start

🤖 Bot:
Welcome to the code.reviewer!
Send me a GitHub link and I’ll review the project.

👤 User: https://github.com/user/project

🤖 Bot:
Analyzing...
✅ Score: Code Quality 75/100 | Docs: 50/100 | CI: 60/100
🧠 Suggestions:
- Add installation instructions to README
- Add basic tests to /core module
- Add a linting step to the CI workflow

---

## 💡 Planned Features
- Async interaction via WebSocket or long polling (in the case with Frontend)
- Support for multi-type languages 
- Support projects history tracking (commits)

--- 

## 📜 License

MIT License — free to use, fork, and modify.  
This project is open-source and designed to evolve with the OSS community.

---

## 🧠 Authors & Vision

This project was founded and is actively developed by [denis-rizun](https://github.com/denis-rizun).  
It is part of a broader initiative to automate and enhance technical code reviews, particularly for open-source contributors, maintainers, and organizations seeking scalable repo evaluation tools.

