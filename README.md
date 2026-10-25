# Terminal Quiz Master

A clean, modular command-line interface (CLI) multiple-choice quiz application built with Python.

## Features

- **Structured Question Bank**: Extensible list of dictionaries representing questions, options (A, B, C, D), and answers.
- **Robust Input Normalization**: Automatically strips whitespace and converts inputs to uppercase, re-prompting on invalid choices.
- **Immediate Visual Feedback**: Displays instant feedback with clear markers and emojis (`✅`, `❌`), showing the correct answer whenever an error is made.
- **Dynamic Score Breakdown**: Computes total correct/incorrect responses, percentage accuracy, and custom tiered feedback.
- **Clean Architecture & PEP 8**: Modular functions (`main`, `run_quiz`, `display_question`, `get_user_choice`, `evaluate_answer`, `display_summary`), clear docstrings, and strict type annotations.

## Requirements

- Python 3.8+ (no third-party dependencies required; uses the Python standard library)

## How to Run

1. Open your terminal and navigate to the project directory:
   ```bash
   cd "/Users/apple/Desktop/udhith repos/terminal-quiz-master"
   ```

2. Run the application:
   ```bash
   python3 quiz_master.py
   ```