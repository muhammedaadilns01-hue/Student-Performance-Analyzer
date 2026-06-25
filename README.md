# Student Performance Analyzer (CLI) 🎓📈

A lightweight, production-ready Command Line Interface (CLI) application built in Python to manage, analyze, and report student performance data. 

This project was built to demonstrate core software engineering principles, including **Separation of Concerns (UI vs. Business Logic)**, **Defensive Programming**, and **Data Integrity Maintenance**.

---

## 🛠️ Key Architectural Features

* **Data Self-Healing:** The system automatically runs a case-insensitive duplicate removal routine on boot to ensure analytical data remains clean.
* **Separation of Concerns:** The entry point (`main.py`) acts purely as an interface controller handling input validation, while `student_manager.py` encapsulates all data manipulation and analytical business logic.
* **Defensive Fault Tolerance:** File I/O operations are wrapped in robust exception handles to gracefully catch missing or corrupted JSON databases without crashing the runtime environment.
* **Tie-Handling Algorithm:** The reporting engine handles analytical edge cases, such as handling score ties cleanly when determining high-performing ranks.

---

## 📁 Project Structure

```text
├── main.py               # Application entry point, CLI loop, & input validation
├── student_manager.py    # Core business logic, data mutation, & analytical engine
├── students.json         # Persistent JSON data store
└── student_performance_report.txt  # Automatically generated analytical report

Prerequisites
Python 3.8 or higher installed on your local machine.

Installation & Execution
Clone this repository to your local workspace:
Bash
git clone [https://github.com/yourusername/student-performance-analyzer.git](https://github.com/yourusername/student-performance-analyzer.git)
cd student-performance-analyzer

Run the application directly using Python:
Bash
python main.py
