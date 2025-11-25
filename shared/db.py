import sqlite3
from pathlib import Path

SCHEMA_VERSION = 1
SCHEMA_SQL = (Path(__file__).parent / "sql" / "schema.sql").read_text()


class Db:
    def __init__(self, path=":memory:"):
        self.connection = sqlite3.connect(path, check_same_thread=False)

        self.migrate()

    def migrate(self):
        """KISS for now"""

        (version,) = self.connection.execute("pragma user_version").fetchone()

        match version:
            case 0:
                # Transaction ?
                self.connection.executescript(SCHEMA_SQL)
                self.connection.commit()
            case version if version == SCHEMA_VERSION:
                # Up to date
                pass
            case other:
                if other != SCHEMA_VERSION:
                    raise RuntimeError(f"Unsupported database version: {other}")

    def get_entry_by_slug(self, slug):
        cursor = self.connection.execute(
            """select 
                id,
                slug,
                body,
                views,
                content_md5_hash,
                user_title,
                user_description,
                user_group,
                user_date_created,
                user_date_modified,
                user_visibility,
                user_draft
            from entries
            where slug = ?
            """,
            (slug,),
        )

        return cursor.fetchone()

    def insert_entry(
        self,
        slug,
        body,
        content_md5_hash,
        user_title,
        user_description,
        user_group,
        user_date_created,
        user_date_modified,
        user_visibility,
        user_draft,
    ):
        self.connection.execute(
            """insert into entries (
                slug,
                body,
                content_md5_hash,
                user_title,
                user_description,
                user_group,
                user_date_created,
                user_date_modified,
                user_visibility,
                user_draft
            ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                slug,
                body,
                content_md5_hash,
                user_title,
                user_description,
                user_group,
                user_date_created,
                user_date_modified,
                user_visibility,
                user_draft,
            ),
        )
        self.connection.commit()
