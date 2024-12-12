# Kanji Trainer for Raspberry Pi

Welcome to the **Kanji Trainer**, an interactive spaced repetition app designed to help you learn Japanese words effectively! The app uses the SM2 algorithm, as described in the [SuperMemo Method](https://www.supermemo.com/en/blog/application-of-a-computer-to-improve-the-results-obtained-in-working-with-the-supermemo-method), to track your daily progress and adapt to your learning pace.

## Features

- **Spaced Repetition System (SRS):** Enhance retention with the SM2 algorithm.
- **Daily Progress Tracking:** Monitor your learning and improve consistently.
- **Database Integration:** Includes the top 3000 most common kanji with stroke order data.

## Getting Started

### Prerequisites

Ensure that your Raspberry Pi is up to date and all required packages are installed. Follow these steps to prepare your environment:

1. **Update Your Raspberry Pi:**

   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Required Libraries and Tools:**
   The project depends on SDL2 for graphical rendering, SDL2-TTF for font rendering, and SQLite for database management. Install these packages using:

   ```bash
   sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-ttf-dev libsdl2-mixer-dev libsqlite3-dev libfreetype6-dev
   ```

3. **Download and Install the Latest SDL (if necessary):**
   If the Raspberry Pi repositories do not have the latest version of SDL (>= 2.28.4), download it from the [SDL GitHub releases page](https://github.com/libsdl-org/SDL/releases). Follow the instructions provided there to build and install SDL from source.

4. **Install Python 3.11:**
   Make sure Python 3.11 is installed on your Raspberry Pi. If it's not already installed, you can compile it from source:

   ```bash
   sudo apt install -y build-essential libssl-dev zlib1g-dev libncurses5-dev libnss3-dev libreadline-dev libffi-dev libbz2-dev
   wget https://www.python.org/ftp/python/3.11.6/Python-3.11.6.tgz
   tar -xvzf Python-3.11.6.tgz
   cd Python-3.11.6
   ./configure --enable-optimizations --enable-loadable-sqlite-extensions
   make -j$(nproc)
   sudo make altinstall
   ```

   After installation, confirm the version:

   ```bash
   python3.11 --version
   ```

5. **Install Poetry:**
   Poetry is used to manage dependencies for this project. Install it using pip:

   ```bash
   python3.11 -m pip install --upgrade pip
   python3.11 -m pip install poetry
   ```

6. **Install Project Dependencies:**
   Navigate to the root project folder and install the dependencies with Poetry:

   ```bash
   poetry install
   ```

   If Poetry fails or you encounter errors, you can export the dependencies to a `requirements.txt` file and install them manually with pip:

   ```bash
   poetry export -f requirements.txt --output requirements.txt
   python3.11 -m pip install -r requirements.txt
   ```

7. **Set Up the Local Database:**
   Follow the instructions provided in the `README` file located in the `/database` folder to properly set up the local database.

## How to Use

1. Launch the application on your Raspberry Pi.
2. Start learning kanji with the interactive spaced repetition system.
3. Track your progress daily and continue building your knowledge.

---

Happy learning!