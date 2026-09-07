import os
from abc import ABC, abstractmethod

import boto3
import pymysql
from dotenv import load_dotenv


load_dotenv()


# ============================================================
# Configuration
# ============================================================

DB_TYPE = os.getenv("DB_TYPE", "mysql").lower()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "knowledgehub")

AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "knowledgehub_items")


# ============================================================
# Repository Interface
# ============================================================

class KnowledgeRepository(ABC):

    @abstractmethod
    def test_connection(self):
        pass

    @abstractmethod
    def create_item(self, title, content):
        pass

    @abstractmethod
    def get_items(self):
        pass


# ============================================================
# MySQL / Aurora Repository
# ============================================================

class MySQLRepository(KnowledgeRepository):

    def __init__(self):
        self.connection = None

    # --------------------------------------------------------
    # Initialize database and tables
    # --------------------------------------------------------

    def initialize_database(self):

        print("Initializing MySQL database...")

        # First connect WITHOUT specifying database
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            autocommit=True
        )

        try:
            with connection.cursor() as cursor:

                # Create database if it doesn't exist
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{MYSQL_DATABASE}`"
                )

                print(
                    f"Database '{MYSQL_DATABASE}' is ready."
                )

        finally:
            connection.close()

        # Now connect to the database
        self.connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            autocommit=True
        )

        # Create tables
        self.create_tables()

    # --------------------------------------------------------
    # Create tables
    # --------------------------------------------------------

    def create_tables(self):

        print("Checking database tables...")

        create_table_query = """
        CREATE TABLE IF NOT EXISTS knowledge_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        with self.connection.cursor() as cursor:
            cursor.execute(create_table_query)

        print("Table 'knowledge_items' is ready.")

    # --------------------------------------------------------
    # Connection test
    # --------------------------------------------------------

    def test_connection(self):

        try:

            if self.connection is None:
                self.initialize_database()

            with self.connection.cursor() as cursor:

                cursor.execute("SELECT 1")

                result = cursor.fetchone()

            print("MySQL connection successful.")

            return result[0] == 1

        except Exception as e:

            print(f"MySQL connection failed: {e}")

            return False

    # --------------------------------------------------------
    # Create item
    # --------------------------------------------------------

    def create_item(self, title, content):

        query = """
        INSERT INTO knowledge_items (title, content)
        VALUES (%s, %s)
        """

        with self.connection.cursor() as cursor:

            cursor.execute(
                query,
                (title, content)
            )

            item_id = cursor.lastrowid

        print(f"Created item with ID: {item_id}")

        return item_id

    # --------------------------------------------------------
    # Get items
    # --------------------------------------------------------

    def get_items(self):

        query = """
        SELECT id, title, content, created_at
        FROM knowledge_items
        ORDER BY created_at DESC
        """

        with self.connection.cursor() as cursor:

            cursor.execute(query)

            items = cursor.fetchall()

        return items


# ============================================================
# DynamoDB Repository
# ============================================================

class DynamoDBRepository(KnowledgeRepository):

    def __init__(self):

        self.dynamodb = boto3.resource(
            "dynamodb",
            region_name=AWS_REGION
        )

        self.table = self.dynamodb.Table(
            DYNAMODB_TABLE
        )

    # --------------------------------------------------------
    # Connection test
    # --------------------------------------------------------

    def test_connection(self):

        try:

            response = self.table.meta.client.describe_table(
                TableName=DYNAMODB_TABLE
            )

            status = response["Table"]["TableStatus"]

            print(
                f"DynamoDB connection successful. "
                f"Table status: {status}"
            )

            return True

        except Exception as e:

            print(f"DynamoDB connection failed: {e}")

            return False

    # --------------------------------------------------------
    # Create item
    # --------------------------------------------------------

    def create_item(self, title, content):

        import uuid

        item_id = str(uuid.uuid4())

        self.table.put_item(
            Item={
                "id": item_id,
                "title": title,
                "content": content
            }
        )

        print(f"Created DynamoDB item: {item_id}")

        return item_id

    # --------------------------------------------------------
    # Get items
    # --------------------------------------------------------

    def get_items(self):

        response = self.table.scan()

        return response.get("Items", [])


# ============================================================
# Repository Factory
# ============================================================

def create_repository():

    if DB_TYPE in ("mysql", "aurora"):

        print(f"Using {DB_TYPE.upper()} repository")

        return MySQLRepository()

    elif DB_TYPE == "dynamodb":

        print("Using DynamoDB repository")

        return DynamoDBRepository()

    else:

        raise ValueError(
            f"Unsupported DB_TYPE: {DB_TYPE}"
        )


# ============================================================
# Main
# ============================================================

def main():

    print("=" * 50)
    print("KnowledgeHub Database Demo")
    print("=" * 50)

    repository = create_repository()

    # Test connection
    if not repository.test_connection():

        print("Database initialization/connection failed.")

        return

    print("\nCreating test item...")

    repository.create_item(
        "AWS RDS Hands-on",
        "Learning RDS MySQL with Python and PyMySQL."
    )

    print("\nFetching items...")

    items = repository.get_items()

    for item in items:

        print(item)

    print("\nDone.")


if __name__ == "__main__":
    main()