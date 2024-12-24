# USCIS N400 Practice Quiz

This project is a Python-based quiz application designed to help individuals practice the 100 USCIS N400 civics questions. It uses a CSV file containing the questions, allows for tracking of correct and incorrect answers, and provides various modes for studying and reviewing the questions.

## Directory Structure

### Main Directories:
- **csv/**: Contains the question data in `.csv` and `.numbers` formats.
- **shell/**: Shell scripts to automate running the quiz in different modes.
- **src/**: Python source code for the quiz application.

### Key Files:
- `uscis_questions.numbers`: The master file for editing the questions. Update state-specific answers here.
- `uscis_questions.csv`: The CSV file generated from the `.numbers` file, used by the quiz application.
- `n400.py`: The main Python script for running the quiz.
- Shell scripts:
  - `n400.sh`: Practice random questions.
  - `n400_all.sh`: Go through all 100 questions.
  - `n400_ask_least.sh`: Practice the least-asked questions.
  - `n400_ask_top.sh`: Practice the most difficult questions.
  - `n400_least.sh`: Display the top 10 least-asked questions.
  - `n400_top.sh`: Display the top 10 most difficult questions.

## Getting Started

### Prerequisites
- Python 3.x
- Pandas library

Install Pandas if not already installed:
```bash
pip install pandas
```

### Setup
1. **Edit State-Specific Answers:**
   - Open `uscis_questions.numbers`.
   - Update the answers to reflect your state's representatives and any other state-specific details.
   - Save the file as a CSV named `uscis_questions.csv` using the script:
     ```bash
     ./uscis_questions.sh
     ```

2. **Run the Quiz:**
   Use one of the provided shell scripts to start the quiz in your preferred mode. Examples:
   - To go through all questions:
     ```bash
     ./n400_all.sh
     ```
   - To practice random questions:
     ```bash
     ./n400.sh
     ```

3. **Tracking Progress:**
   The quiz tracks how many times each question is answered correctly (`g`) and incorrectly (`b`). This data is saved to `uscis_questions.csv` after every session.

### Quiz Modes
- **Random Mode (`n400.sh`)**: Selects random questions with weighted probabilities based on past performance (prioritizing harder questions).
- **All Questions Mode (`n400_all.sh`)**: Sequentially goes through all 100 questions.
- **Top 10 Difficult Questions (`n400_top.sh`)**: Displays the 10 questions with the highest failure rates.
- **Top 10 Least Asked Questions (`n400_least.sh`)**: Displays the 10 questions asked the fewest times.
- **Practice Top Difficult Questions (`n400_ask_top.sh`)**: Asks the top 10 most failed questions.
- **Practice Least Asked Questions (`n400_ask_least.sh`)**: Asks the top 10 least asked questions.

## How to Use the Application
1. Start by editing the `.numbers` file with state-specific details.
2. Convert the `.numbers` file into a CSV using `uscis_questions.sh`.
3. Use one of the provided shell scripts to practice questions.

During each session, the following features are available:
- Questions are displayed with a unique ID.
- User answers are normalized to account for minor variations in wording.
- Feedback is provided on whether the answer is correct or incorrect.
- Statistics on total questions, correct answers, and performance percentage are displayed.

### Example Commands
- To display the top 10 difficult questions:
  ```bash
  ./n400_top.sh
  ```
- To practice the least-asked questions:
  ```bash
  ./n400_ask_least.sh
  ```

## ANSI Colors
The quiz uses ANSI escape codes to colorize the terminal output:
- **Green**: Correct answers.
- **Red**: Incorrect answers.
- **Grey**: Progress and statistics.

## Notes
- Always save progress after each session to ensure your statistics are updated.
- If you need to exit mid-session, use `Ctrl+C`. Progress will be saved automatically.

## Author
Developed by Jordi Torras. For inquiries or suggestions, please contact [your email or website].

