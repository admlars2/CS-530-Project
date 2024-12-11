from ..database import StudyCardDB, WordDatabase
from ..config import STUDY_CARD_DB_PATH, LEARNING_SETTINGS

class DBManager:
    def __init__(self):
        """
        DBManager allows for operations that involve both of the databases and their interactions.
        """
        self.word_db = WordDatabase()
        self.study_card_db = StudyCardDB()
        self.num_new = 0
        self.num_study_cards = 0

    def close(self):
        """
        Closes both databases.
        """
        self.word_db.close()
        self.study_card_db.close()

    def generate_and_insert_new_cards(self, limit):
        """
        Generates and inserts new study cards from the Words database
        into the StudyCards database.

        Args:
            limit (int): Maximum number of new word IDs to process.
        """
        self.word_db.cursor.execute(f"ATTACH DATABASE '{STUDY_CARD_DB_PATH}' AS study_db;")

        query = """
        SELECT w.id
        FROM Words w
        LEFT JOIN study_db.StudyCards sc ON w.id = sc.card_id
        WHERE sc.card_id IS NULL
        ORDER BY w.frequency ASC
        LIMIT ?;
        """
        params = (limit,)
        self.word_db.cursor.execute(query, params)
        results = self.word_db.cursor.fetchall()
        new_card_ids = [row[0] for row in results]
        self.word_db.cursor.execute("DETACH DATABASE study_db;")

        for card_id in new_card_ids:
            self.study_card_db.add_card(card_id, reversed=False)
            self.study_card_db.add_card(card_id, reversed=True)

    def count_cards(self):
        self.num_study_cards = self.study_card_db.count_due_cards()
        self.num_new = 0

    def aggregate_cards(self):
        """
        Aggregates the cards for the current session by:
        1. Counting all due cards from the StudyCards database.
        2. Generating new cards if the number of due cards is less than the configured new card limit.
        """
        self.num_study_cards = self.study_card_db.count_due_cards()
        self.num_new = max(0, LEARNING_SETTINGS["new_card_limit"] - self.num_study_cards) * 2

        if self.num_new > 0:
            self.generate_and_insert_new_cards(self.num_new)

    def review_card_get_next(self, card_id, quality):
        """
        Reviews the current card and fetches the next due card.

        Args:
            card_id (int): The ID of the card being reviewed.
            quality (int): The review quality (1-4).

        Returns:
            dict: The next due card's details.
        """
        self.study_card_db.update_card_review(card_id, quality)
        return self.study_card_db.get_next_due_card()