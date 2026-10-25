#!/usr/bin/env python3
"""
Terminal Quiz Master
====================
A clean, modular, and interactive command-line quiz application.

Demonstrates:
- Structured data using lists of dictionaries
- Robust input handling and normalization
- Separation of concerns across modular functions
- PEP 8 compliance, type hints, and comprehensive docstrings
"""

import sys
from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# Data Structure: Quiz Questions
# ---------------------------------------------------------------------------
# Each question is represented as a dictionary containing:
# - "prompt": The question text
# - "options": A dictionary mapping choice letters to text
# - "answer": The correct option key (uppercase)
# ---------------------------------------------------------------------------
QUESTIONS: List[Dict[str, Any]] = [
    {
        "prompt": "What is the primary purpose of Python's 'self' keyword in class methods?",
        "options": {
            "A": "It refers to the current instance of the class.",
            "B": "It declares a variable as private to the module.",
            "C": "It is a built-in function that creates object singletons.",
            "D": "It links subclasses to their parent class.",
        },
        "answer": "A",
    },
    {
        "prompt": "Which built-in Python data structure is mutable and maintains insertion order?",
        "options": {
            "A": "Tuple",
            "B": "List",
            "C": "Frozenset",
            "D": "Integer",
        },
        "answer": "B",
    },
    {
        "prompt": "What does the expression `bool([])` evaluate to in Python?",
        "options": {
            "A": "True",
            "B": "False",
            "C": "None",
            "D": "Raises a TypeError",
        },
        "answer": "B",
    },
    {
        "prompt": "Which keyword is used to handle exceptions caught by a `try` block?",
        "options": {
            "A": "catch",
            "B": "handle",
            "C": "except",
            "D": "rescue",
        },
        "answer": "C",
    },
    {
        "prompt": "What is the time complexity of searching for a key in a standard Python dictionary (average case)?",
        "options": {
            "A": "O(n)",
            "B": "O(log n)",
            "C": "O(1)",
            "D": "O(n log n)",
        },
        "answer": "C",
    },
]


# ---------------------------------------------------------------------------
# UI & Formatting Helpers
# ---------------------------------------------------------------------------
def print_banner(title: str) -> None:
    """Print an eye-catching decorative banner for headers."""
    divider = "=" * 60
    print(f"\n{divider}")
    print(f" {title.center(58)} ")
    print(f"{divider}\n")


def display_question(
    current_idx: int,
    total_count: int,
    question_data: Dict[str, Any],
) -> None:
    """
    Print the question number, prompt, and multiple-choice options.

    :param current_idx: Current 1-based index of the question.
    :param total_count: Total number of questions in the quiz.
    :param question_data: Dictionary containing prompt and options.
    """
    print("-" * 60)
    print(f"📝 Question {current_idx} of {total_count}")
    print("-" * 60)
    print(f"{question_data['prompt']}\n")

    options: Dict[str, str] = question_data["options"]
    for key in sorted(options.keys()):
        print(f"  [{key}] {options[key]}")
    print()


# ---------------------------------------------------------------------------
# Input Normalization & Validation
# ---------------------------------------------------------------------------
def get_user_choice(valid_options: List[str]) -> str:
    """
    Prompt the user for input, normalize it, and validate against allowed options.

    Normalizes input by trimming leading/trailing whitespace and converting
    to uppercase. Loops continuously until valid input or an exit signal is received.

    :param valid_options: A list of acceptable option keys (e.g. ['A', 'B', 'C', 'D']).
    :return: A validated, uppercase string matching one of the options.
    """
    formatted_valid = ", ".join(valid_options)
    while True:
        try:
            raw_input = input(f"👉 Enter your choice ({formatted_valid}): ")
        except (KeyboardInterrupt, EOFError):
            print("\n\nQuiz cancelled by user. Goodbye! 👋")
            sys.exit(0)

        # Normalize: strip surrounding whitespace and convert to uppercase
        cleaned_choice = raw_input.strip().upper()

        if cleaned_choice in valid_options:
            return cleaned_choice

        print(
            f"⚠️  Invalid choice '{raw_input.strip()}'. "
            f"Please enter one of: {formatted_valid}.\n"
        )


# ---------------------------------------------------------------------------
# Feedback & Evaluation
# ---------------------------------------------------------------------------
def evaluate_answer(user_choice: str, question_data: Dict[str, Any]) -> bool:
    """
    Evaluate user choice against the correct answer and display immediate feedback.

    :param user_choice: The normalized user response letter.
    :param question_data: Dictionary containing 'answer' and 'options'.
    :return: True if the answer was correct, False otherwise.
    """
    correct_key: str = question_data["answer"].upper()
    options: Dict[str, str] = question_data["options"]
    correct_text: str = options.get(correct_key, "")

    if user_choice == correct_key:
        print("\n✅ Correct! Well done! 🎉\n")
        return True

    print("\n❌ Incorrect!")
    print(f"   Correct Answer: [{correct_key}] {correct_text}\n")
    return False


# ---------------------------------------------------------------------------
# Summary & Performance Evaluation
# ---------------------------------------------------------------------------
def get_performance_tier(percentage: float) -> str:
    """
    Determine a personalized feedback message based on percentage score.

    :param percentage: Score as a percentage (0.0 to 100.0).
    :return: A feedback message reflecting performance tier.
    """
    if percentage == 100.0:
        return "🏆 Flawless Victory! You have mastered this topic!"
    elif percentage >= 80.0:
        return "🌟 Outstanding Performance! Great understanding of the fundamentals!"
    elif percentage >= 60.0:
        return "👍 Solid Effort! A little more practice and you will be a master."
    elif percentage >= 40.0:
        return "📚 Keep Learning! Review the explanations and try again."
    else:
        return "💡 Don't give up! Consistent practice is the key to mastery."


def display_summary(score: int, total_questions: int) -> None:
    """
    Display a comprehensive score breakdown and final remarks.

    :param score: Number of correct answers.
    :param total_questions: Total number of questions presented.
    """
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0.0
    tier_message = get_performance_tier(percentage)

    print_banner("QUIZ SUMMARY & RESULTS")
    print(f"  • Total Questions:   {total_questions}")
    print(f"  • Correct Answers:   {score}")
    print(f"  • Incorrect Answers: {total_questions - score}")
    print(f"  • Final Score:       {percentage:.1f}%")
    print("-" * 60)
    print(f"  {tier_message}")
    print("=" * 60 + "\n")


# ---------------------------------------------------------------------------
# Core Game Loop
# ---------------------------------------------------------------------------
def run_quiz(questions: List[Dict[str, Any]]) -> None:
    """
    Manage the sequential flow of the quiz from start to finish.

    :param questions: List of question dictionaries to run.
    """
    if not questions:
        print("No questions found in the quiz database.")
        return

    print_banner("WELCOME TO TERMINAL QUIZ MASTER")
    print("Test your Python knowledge with multiple-choice questions!")
    print("Read each question carefully and type your chosen option (A/B/C/D).\n")

    score = 0
    total = len(questions)

    for idx, q_data in enumerate(questions, start=1):
        display_question(current_idx=idx, total_count=total, question_data=q_data)
        valid_keys = sorted(q_data["options"].keys())
        choice = get_user_choice(valid_options=valid_keys)

        if evaluate_answer(user_choice=choice, question_data=q_data):
            score += 1

    display_summary(score=score, total_questions=total)


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------
def main() -> None:
    """Application entry point."""
    run_quiz(QUESTIONS)


if __name__ == "__main__":
    main()
