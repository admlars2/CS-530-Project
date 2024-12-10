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
        Updates the user's streak, best streak, and last login.
        
        Logic:
        - If it's the user's first login (no last_login), initialize streak to 1.
        - If the user logs in on the same day, do not change the streak.
        - If the user logs in exactly one day after their last login, increment the streak.
        - If the user logs in after more than one day since the last login, reset the streak to 1.
        - Update the best streak if the current streak surpasses it.
        """
        current_date = datetime.now().date()

        if self.last_login is None:
            # First login
            self.daily_streak = 1
        else:
            delta_days = (current_date - self.last_login).days
            if delta_days == 0:
                # Same day login, no change
                pass
            elif delta_days == 1:
                # Consecutive day login, increment streak
                self.daily_streak += 1
            else:
                # Missed a day or more, reset streak
                self.daily_streak = 1

        # Update the best streak if needed
        if self.daily_streak > self.best_streak:
            self.best_streak = self.daily_streak

        # Set the last_login to today
        self.last_login = current_date

        # Update the database
        self.cursor.execute("""
            UPDATE Config
            SET daily_streak = ?, last_login = ?, best_streak = ?
            WHERE id = 1
        """, (self.daily_streak, self.last_login, self.best_streak))
        self.conn.commit()

        return self.daily_streak, self.best_streak

    def count_due_cards(self) -> int:
        """
        Counts the number of due cards in the database.

        Returns:
            int: The number of due cards.
        """
        self.cursor.execute("""
            SELECT COUNT(*)
            FROM StudyCards
            WHERE due_date <= ?
        """, (datetime.now().date(),))
        return self.cursor.fetchone()[0]

    def get_next_due_card(self) -> dict:
        """
        Retrieves the next due card for review.

        Returns:
            dict: The next card's details.
        """
        self.cursor.execute("""
            SELECT * 
            FROM StudyCards
            WHERE due_date <= ?
            ORDER BY due_date ASC
            LIMIT 1
        """, (datetime.now().date(),))
        result = self.cursor.fetchone()
        if not result:
            return None  # No due cards
        column_names = [description[0] for description in self.cursor.description]
        return dict(zip(column_names, result))

    def add_card(self, card_id: int, reversed: bool = False) -> None:
        """
        Adds a new card to the database.

        Args:
            card_id (int): The ID of the card (e.g., word ID from kanji.db).
            reversed (bool): Whether the card is reversed (default is False).
        """
        self.cursor.execute("""
            INSERT INTO StudyCards (card_id, reversed, due_date)
            VALUES (?, ?, ?)
        """, (card_id, reversed, datetime.now().date()))
        self.conn.commit()

    def update_card_review(self, card_id: int, quality: int) -> None:
        """
        Updates a card after it has been reviewed.

        Args:
            card_id (int): The ID of the card being reviewed.
            quality (int): The review quality (1-4).
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