from copy import deepcopy
from os import getenv
from random import randint
from logging import getLogger
from dotenv import load_dotenv
from psycopg2 import connect, Error, DatabaseError
from psycopg2.extras import execute_values

load_dotenv()


class QuoteGetter:
    # database connection related variables
    DB_USER = ""
    DB_PASS = ""
    DB_SERVER = ""
    DB = ""
    cursor = None
    connection = None

    # for the source of truth - the list and the length of the list
    ORIGINAL_DATA = []
    ORIGINAL_DATA_LENGTH = 0

    UP_FOR_RELEASE = []  # pool of quotes that have not been said by the bot
    released = 0  # refers to the number of quotes released in the current session

    logger = None

    def __init__(self):
        self.logger = getLogger(__name__)

        self.DB_USER = getenv("DB_USER")
        self.DB_PASS = getenv("DB_PASS")
        self.DB_SERVER = getenv("DB_SERVER")
        self.DB = getenv("DB")
        self.connect_db()
        self.setup_data()

    def connect_db(self):
        # trying here to connect to the existing database
        try:
            self.connection = connect(
                user=self.DB_USER,
                password=self.DB_PASS,
                host=self.DB_SERVER,
                port="5432",
                database="xdy_bot",
            )
            # disabling auto-commit so that in case of a transaction failure, we can roll back
            self.connection.autocommit = False
            # setting cursor to perform database operations
            self.cursor = self.connection.cursor()
        except (Exception, Error) as error:
            self.logger.error(f"Error while trying to connect to PostgreSQL - {error}")
        finally:
            self.logger.debug("Done trying to connect to PostgreSQL...")

    def get_connection_info(self):
        # logging current PostgreSQL details
        self.logger.info("Logging PostgreSQL server information")
        self.logger.info(self.connection.get_dsn_parameters())
        self.cursor.execute("SELECT version();")
        record = self.cursor.fetchone()
        self.logger.info(f"You are connected to - {record}")

    def store_quotes_up_for_release(self):
        self.logger.info("Processing quotes up for release...")
        try:
            # delete everything in the current table
            self.cursor.execute("DELETE FROM quotes_up_for_release")
            # insert current quotes up for release
            up_for_release_list = list(map(lambda x: (x[1], x[2]), self.UP_FOR_RELEASE))
            execute_values(
                self.cursor,
                "INSERT INTO quotes_up_for_release (incoming_quote, incoming_context) VALUES %s",
                up_for_release_list,
            )
            self.connection.commit()
        except (Exception, DatabaseError) as error:
            self.logger.error(
                f"Error in transaction when inserting used quote to database: {error}"
            )
            self.connection.rollback()
        finally:
            self.logger.debug("Done processing quotes up for release...")

    def store_inserted_quote(self, quote):
        # database-related code
        try:
            self.logger.info("Inserting released quote to database...")
            # creating this to handle apostrophes when inserting in PostgreSQL
            inserted_quote = quote["quote"].replace("'", "''")
            inserted_context = quote["context"].replace("'", "''")
            # inserting quote and committing the changes
            self.cursor.execute(
                f"INSERT INTO used_quotes (used_quote, used_context) VALUES ('{inserted_quote}', '{inserted_context}')"
            )
            self.connection.commit()
        except (Exception, DatabaseError) as error:
            self.logger.error(
                f"Error in transaction when inserting used quote to database: {error}"
            )
            self.connection.rollback()
        finally:
            self.logger.debug("Done processing released quote to database...")

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.logger.debug("PostgreSQL connection successfully closed...")

    def setup_data(self):
        # execute query for getting all the quotes
        self.cursor.execute("SELECT * FROM all_quotes")
        self.ORIGINAL_DATA = self.cursor.fetchall()
        self.ORIGINAL_DATA_LENGTH = len(self.ORIGINAL_DATA)
        # execute query for getting all quotes up for release
        self.cursor.execute("SELECT * FROM quotes_up_for_release")
        self.UP_FOR_RELEASE = self.cursor.fetchall()
        # if empty, basically copy the source of truth as this means that all quotes have been released
        if not self.UP_FOR_RELEASE:
            self.UP_FOR_RELEASE = deepcopy(self.ORIGINAL_DATA)
        # source of truth - up for release
        self.released = self.ORIGINAL_DATA_LENGTH - len(self.UP_FOR_RELEASE)

    # pooling implementation here
    def get_quote(self):
        # setting up dictionary [object] for the quote
        quote = {"quote": "", "context": ""}

        # getting the random quote happens here
        random_index_for_release = randint(0, len(self.UP_FOR_RELEASE) - 1)
        quote_released = self.UP_FOR_RELEASE.pop(random_index_for_release)
        quote["quote"] = quote_released[1]
        quote["context"] = quote_released[2]

        # adding to the released counter the random quote that was popped
        self.released = self.released + 1
        up_for_release_remaining = len(self.UP_FOR_RELEASE)

        # Logging how many quotes are left per pool
        self.logger.debug(
            f"Currently {up_for_release_remaining} quote/s remaining to be said..."
        )
        self.logger.debug(f"Currently {self.released} quote/s said...")

        # logic for resetting pool happens here
        if self.released == self.ORIGINAL_DATA_LENGTH:
            self.logger.info(
                "All Xander quotes in the repository have been said... Resetting pool..."
            )
            self.UP_FOR_RELEASE = deepcopy(self.ORIGINAL_DATA)

        self.logger.info("Successfully got a random Xander quote...")
        return quote

    def get_up_for_release_quotes_length(self):
        return len(self.UP_FOR_RELEASE)

    def get_released_quotes_length(self):
        return self.released
