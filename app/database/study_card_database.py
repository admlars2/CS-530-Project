import sqlite3
from datetime import datetime, timedelta
from ..config import STUDY_CARD_DB_PATH, LEARNING_SETTINGS

class StudyCardDB:
    def __init__(self):
        self.conn = sqlite3.connect(STUDY_CARD_DB_PATH)
        self.cursor = self.conn.cursor()

        # Cache variables
        self.current_date = datetime.now().date()
        self.daily_streak = None
        self.best_streak = None
        self.last_login = None

        # Initialize cache from database
        self._initialize_cache()

    def _initialize_cache(self):
        """Initialize the cached values from the database."""
        self.cursor.execute("""
            SELECT daily_streak, last_login, best_streak
            FROM Config
            WHERE id = 1
        """)
        result = self.cursor.fetchone()
        if result:
            self.daily_streak, self.last_login, self.best_streak = result
            if self.last_login:
                self.last_login = datetime.strptime(self.last_login, "%Y-%m-%d").date()
        else:
            raise Exception("Config table is not initialized with a user.")

    def close(self):
        """Closes the database connection."""
        self.conn.close()

    def update_login_and_streak(self) -> tuple[int, int]:
        """
        Updates the user's streak, max streak, and last login.
        - If the user logs in on a consecutive day, the streak increases.
        - If the user skips a day, the streak resets to 1.
        - The max streak is updated if the current streak exceeds it.
        """
        # Check if the date has changed during the session
        current_date = datetime.now().date()

        # Update cache and determine streak logic
        if self.last_login:
            if current_date == self.last_login + timedelta(days=1):
                # Consecutive day login, increase streak
                self.daily_streak += 1
            else:
                # Missed a day, reset streak
                self.daily_streak = 1
        else:
            # First-time login
            self.daily_streak = 1

        # Update best streak if current streak exceeds it
        if self.daily_streak > self.best_streak:
            self.best_streak = self.daily_streak

        # Update cache and database
        self.last_login = current_date
        self.current_date = current_date

        self.cursor.execute("""
            UPDATE Config
            SET daily_streak = ?, last_login = ?, best_streak = ?
            WHERE id = 1
        """, (self.daily_streak, self.last_login, self.best_streak))
        self.conn.commit()

        return self.daily_streak, self.best_streak
    
    def add_card(self, card_id: int, reversed: bool = False) -> int:
        """
        Adds a new card to the database.
        :param card_id: The ID of the card (e.g., word ID from kanji.db).
        :param reversed: Whether the card is reversed (default is False).
        :return: The ID of the newly created card.
        """
        self.cursor.execute("""
            INSERT INTO StudyCards (card_id, reversed, due_date)
            VALUES (?, ?, ?)
        """, (card_id, reversed, datetime.now().date()))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_due_cards(self) -> list[dict]:
        """
        Retrieves all cards that are due for review.
        :return: A list of tuples containing card information.
        """
        self.cursor.execute("""
            SELECT * FROM StudyCards
            WHERE due_date <= ?
        """, (datetime.now().date(),))
        results = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]
        
        return [dict(zip(column_names, row)) for row in results]

    def update_card_review(self, card_id: int, quality: int) -> None:
        """
        Updates a card after it has been reviewed.
        :param card_id: The ID of the card being reviewed.
        :param quality: The review quality (1–4).
        """
        self.cursor.execute("""
            SELECT interval, ease_factor, review_count
            FROM StudyCards
            WHERE id = ?
        """, (card_id,))
        card = self.cursor.fetchone()
        if not card:
            raise ValueError("Card not found.")

        interval, ease_factor, review_count = card

        # Load settings from LEARNING_SETTINGS
        min_ease_factor = LEARNING_SETTINGS["min_ease_factor"]
        lapse_interval_factor = LEARNING_SETTINGS["lapse_interval_factor"]

        # Adjust ease factor based on quality
        ease_factor = max(min_ease_factor, ease_factor + (0.1 - (3 - quality) * (0.08 + (3 - quality) * 0.02)))

        # Update interval based on quality and settings
        if quality < LEARNING_SETTINGS["quality_threshold"]:
            interval = max(1, int(interval * lapse_interval_factor))  # Reset or reduce interval
        else:
            interval = int(interval * ease_factor)
            interval = min(interval, LEARNING_SETTINGS["max_interval"])  # Cap interval to max_interval

        # Update card attributes
        due_date = datetime.now().date() + timedelta(days=interval)
        review_count += 1

        self.cursor.execute("""
            UPDATE StudyCards
            SET interval = ?, ease_factor = ?, review_count = ?, due_date = ?, last_quality = ?, last_studied = ?
            WHERE id = ?
        """, (interval, ease_factor, review_count, due_date, quality, datetime.now().date(), card_id))
        self.conn.commit()

    def get_all_cards(self) -> list[tuple]:
        """
        Retrieves all cards in the database.
        :return: A list of tuples containing card information.
        """
        self.cursor.execute("SELECT * FROM StudyCards")
        results = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]
        return [dict(zip(column_names, row)) for row in results]