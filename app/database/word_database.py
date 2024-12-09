import sqlite3
from ..config import DATABASE_PATH, ENGLISH, JAPANESE

class WordDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def search(self, term, mode=ENGLISH, limit=3):
        if mode == ENGLISH:
            query = """
            SELECT *
            FROM Words
            WHERE translations LIKE ?
            ORDER BY
                CASE
                    WHEN translations = ? THEN 1                                    -- Exact match priority
                    WHEN ' ' || translations || ' ' LIKE '% ' || ? || ' %' THEN 2   -- Word found in translation
                    WHEN translations LIKE ? THEN 3                                 -- Partial match priority
                    ELSE 4                                                          -- Lowest priority
                END,
                frequency DESC                                                      -- Secondary sort by frequency
            LIMIT ?;
            """
            params = (f"%{term}%", term, term, f"%{term}%", limit)
        elif mode == JAPANESE:
            query = """
            SELECT *
            FROM Words
            WHERE reading LIKE ?
            LIMIT ?;
            """
            params = (f"%{term}%", limit)
        else:
            raise ValueError("Invalid mode. Use ENGLISH or JAPANESE.")
        
        # Execute the query with the provided parameters
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()

        # Get column names for better formatting
        column_names = [description[0] for description in self.cursor.description]

        # Format results as a list of dictionaries
        return [dict(zip(column_names, row)) for row in results]