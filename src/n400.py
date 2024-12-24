import pandas as pd
import random
import sys

# File path
file_path = "../csv/uscis_questions.csv"

# ANSI escape codes for colors
GREEN = "\033[92m"  # Bright Green
RED = "\033[91m"    # Bright Red
GREY = "\033[90m"   # Grey (Dim)
RESET = "\033[0m"   # Reset to default color

# Load the questions from the CSV
def load_questions(file_path):
    return pd.read_csv(file_path)

# Save updated questions back to the CSV
def save_questions(df, file_path):
    df.to_csv(file_path, index=False)

# Normalize the answer
def normalize_answer(answer):
    words_to_ignore = {
        "the", "and", "a", "in", "to", "for", "or", "of", 
        "on", "at", "by", "with", "as", "an", "is", "it", 
        "that", "this", "these", "those", "be", "am", "are", 
        "was", "were", "been", "has", "have", "had", "do", 
        "does", "did", "not", "but", "if", "then", "else", 
        "from", "over", "under", "out", "about", "up", "down", 
        "into", "after", "before", "while", "during"
    }
    words = answer.split()
    normalized_words = [word.rstrip('s') for word in words if word not in words_to_ignore]
    return set(normalized_words)

# Ask a single question
def ask_question(df, index, session_stats, progress=None):
    question_id = df.loc[index, 'id']
    question = df.loc[index, 'question']
    correct_answer = df.loc[index, 'answer'].strip().lower()

    # Display progress if provided
    if progress:
        current, total = progress
        correct = session_stats["correct_answers"]
        percentage = (correct / (current if current > 0 else 1)) * 100  # Fix percentage calculation
        print(f"{GREY}Progress: ({current}/{total}) | Correct: {percentage:.2f}%{RESET}")

    print(f"({question_id}) {question}")

    user_answer = ""
    while not user_answer.strip():  # Ensure a non-empty answer
        try:
            user_answer = input("Your answer: ").strip().lower()
            if not user_answer:
                print(f"{RED}Answer cannot be empty. Please try again.{RESET}")
        except EOFError:
            print("\nExiting... Saving progress.")
            save_questions(df, file_path)
            sys.exit(0)

    # Normalize answers
    correct_words = normalize_answer(correct_answer)
    user_words = normalize_answer(user_answer)

    # Update statistics
    session_stats["total_questions"] += 1
    if correct_words == user_words:
        print(f"{GREEN}Correct! The correct answer is: {correct_answer}{RESET}")
        df.at[index, 'g'] += 1
        session_stats["correct_answers"] += 1
    else:
        print(f"{RED}Wrong! The correct answer is: {correct_answer}{RESET}")
        df.at[index, 'b'] += 1

    # Save progress immediately
    save_questions(df, file_path)
    
# Main loop for `-all` mode
def quiz_all_mode(df, file_path):
    session_stats = {"total_questions": 0, "correct_answers": 0}
    question_indices = list(df.index)
    random.shuffle(question_indices)  # Shuffle questions

    total_questions = len(question_indices)
    for current_index, index in enumerate(question_indices, start=1):
        try:
            ask_question(df, index, session_stats, progress=(current_index, total_questions))
        except EOFError:
            print("\nExiting... Saving progress.")
            save_questions(df, file_path)
            sys.exit(0)

    # Display final statistics
    correct = session_stats["correct_answers"]
    total = session_stats["total_questions"]
    percentage = (correct / total) * 100 if total > 0 else 0
    print(f"{GREY}Final Stats: Total Questions: {total}, Correct Answers: {correct}, Percentage: {percentage:.2f}%{RESET}")

# Main loop for normal mode
def quiz_loop(file_path):
    df = load_questions(file_path)
    session_stats = {"total_questions": 0, "correct_answers": 0}

    while True:
        try:
            # Select a question randomly based on weights
            weights = (df['b'] + 1) / ((df['g'] + df['b']) + 1)
            selected_index = random.choices(df.index, weights=weights, k=1)[0]
            ask_question(df, selected_index, session_stats)
        except KeyboardInterrupt:
            print("\nExiting... Saving progress.")
            save_questions(df, file_path)
            sys.exit(0)

# Display top 10 most difficult questions
def top_difficult_questions(df):
    print(f"{RED}Top 10 Most Difficult Questions:{RESET}")
    df['failure_rate'] = df['b'] / (df['g'] + df['b']).replace(0, 1)
    top_df = df.sort_values(by='failure_rate', ascending=False).head(10)
    for _, row in top_df.iterrows():
        question_id = row['id']
        question = row['question']
        failure_rate = row['failure_rate'] * 100
        print(f"({question_id}) {question} - Failure Rate: {failure_rate:.2f}%")

# Display top 10 least asked questions
def least_asked_questions(df):
    print(f"{GREEN}Top 10 Least Asked Questions:{RESET}")
    df['total_asked'] = df['g'] + df['b']
    least_asked_df = df.sort_values(by='total_asked', ascending=True).head(10)
    for _, row in least_asked_df.iterrows():
        question_id = row['id']
        question = row['question']
        total_asked = row['total_asked']
        print(f"({question_id}) {question} - Times Asked: {total_asked}")

# Ask the 10 least asked questions
def ask_least_asked_questions(df, file_path):
    session_stats = {"total_questions": 0, "correct_answers": 0}
    df['total_asked'] = df['g'] + df['b']
    least_asked_df = df.sort_values(by='total_asked', ascending=True).head(10)
    question_indices = least_asked_df.index

    for current_index, index in enumerate(question_indices, start=1):
        try:
            ask_question(df, index, session_stats, progress=(current_index, len(question_indices)))
        except EOFError:
            print("\nExiting... Saving progress.")
            save_questions(df, file_path)
            sys.exit(0)

    # Display final statistics
    correct = session_stats["correct_answers"]
    total = session_stats["total_questions"]
    percentage = (correct / total) * 100 if total > 0 else 0
    print(f"{GREY}Final Stats: Total Questions: {total}, Correct Answers: {correct}, Percentage: {percentage:.2f}%{RESET}")

# Ask the top 10 most failed questions
def ask_top_failed_questions(df, file_path):
    session_stats = {"total_questions": 0, "correct_answers": 0}
    df['failure_rate'] = df['b'] / (df['g'] + df['b']).replace(0, 1)
    top_failed_df = df.sort_values(by='failure_rate', ascending=False).head(10)
    question_indices = top_failed_df.index

    for current_index, index in enumerate(question_indices, start=1):
        try:
            ask_question(df, index, session_stats, progress=(current_index, len(question_indices)))
        except EOFError:
            print("\nExiting... Saving progress.")
            save_questions(df, file_path)
            sys.exit(0)

    # Display final statistics
    correct = session_stats["correct_answers"]
    total = session_stats["total_questions"]
    percentage = (correct / total) * 100 if total > 0 else 0
    print(f"{GREY}Final Stats: Total Questions: {total}, Correct Answers: {correct}, Percentage: {percentage:.2f}%{RESET}")

# Entry point
if __name__ == "__main__":
    df = load_questions(file_path)

    if len(sys.argv) > 1:
        if sys.argv[1] == "-all":
            quiz_all_mode(df, file_path)
        elif sys.argv[1] == "-top":
            top_difficult_questions(df)
        elif sys.argv[1] == "-least":
            least_asked_questions(df)
        elif sys.argv[1] == "-ask_least":
            ask_least_asked_questions(df, file_path)
        elif sys.argv[1] == "-ask_top":
            ask_top_failed_questions(df, file_path)
        else:
            quiz_loop(file_path)
    else:
        quiz_loop(file_path)
