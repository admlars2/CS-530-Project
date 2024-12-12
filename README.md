# Kanji Trainer for Raspberry Pi

Welcome to the **Kanji Trainer**, an interactive spaced repetition app designed to help you learn Japanese words effectively! The app uses the SM2 algorithm, as described in the [SuperMemo Method](https://www.supermemo.com/en/blog/application-of-a-computer-to-improve-the-results-obtained-in-working-with-the-supermemo-method), to track your daily progress and adapt to your learning pace.

## Features
- **Spaced Repetition System (SRS):** Enhance retention with the SM2 algorithm.
- **Daily Progress Tracking:** Monitor your learning and improve consistently.
- **Database Integration:** Includes the top 2000 most common kanji with stroke order data.

## Getting Started
### Prerequisites
Ensure that your Raspberry Pi is up to date and all required packages are installed. Follow these steps to prepare your environment:

1. **Update Your Raspberry Pi:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Python 3.11:**
   Make sure Python 3.11 is installed on your Raspberry Pi. If not, install it using:
   ```bash
   sudo apt install python3.11
   ```

3. **Download and Install the Latest SDL:**
   This project requires the latest version of SDL. You can download it from the [SDL GitHub releases page](https://github.com/libsdl-org/SDL/releases). Follow the instructions provided on the page to install SDL on your Raspberry Pi.

4. **Install Poetry:**
   Poetry is used to manage dependencies for this project. Install it with pip:
   ```bash
   pip install poetry
   ```

5. **Install Project Dependencies:**
   Navigate to the root project folder and run:
   ```bash
   poetry install
   ```

6. **Set Up the Local Database:**
   Follow the instructions provided in the `README` file located in the `/database` folder to properly set up the local database.

## How to Use
1. Launch the application on your Raspberry Pi.
2. Start learning kanji with the interactive spaced repetition system.
3. Track your progress daily and continue building your knowledge.

---
Happy learning!