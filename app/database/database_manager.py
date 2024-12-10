from ..database import StudyCardDB, WordDatabase
from ..config import STUDY_CARD_DB_PATH, LEARNING_SETTINGS

class DBManager:
    def __init__(self):
        self.word_db = WordDatabase()
        self.study_card_db = StudyCardDB()

    def close(self):
        """Closes both Word and StudyCard database connections."""
        self.word_db.close()
        self.study_card_db.close()

    def generate_and_insert_new_cards(self):
        """
        Selects new word IDs from the Words database that are not yet in the StudyCards table,
        and inserts them into the StudyCards table with normal and reversed entries.
        """
        # Attach the StudyCards database to the Words database
        self.word_db.cursor.execute(f"ATTACH DATABASE '{STUDY_CARD_DB_PATH}' AS study_db;")

        # Query to find new word IDs
        query = """
        SELECT w.id
        FROM Words w
        LEFT JOIN study_db.StudyCards sc ON w.id = sc.card_id
        WHERE sc.card_id IS NULL
        ORDER BY w.frequency DESC
        LIMIT ?;
        """
        params = (LEARNING_SETTINGS["new_card_limit"],)

        # Execute the query
        self.word_db.cursor.execute(query, params)
        results = self.word_db.cursor.fetchall()

        # Extract IDs from the results
        new_card_ids = [row[0] for row in results]

        # Detach the StudyCards database
        self.word_db.cursor.execute("DETACH DATABASE study_db;")

        # Insert new cards into the StudyCards table
        for card_id in new_card_ids:
            self.study_card_db.add_card(card_id=card_id, reversed=False)  # Normal card
            self.study_card_db.add_card(card_id=card_id, reversed=True)   # Reversed card