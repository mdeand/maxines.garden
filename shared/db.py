import sqlite3
from pathlib import Path

SCHEMA_VERSION = 1
SCHEMA_SQL = (Path(__file__).parent / "sql" / "schema.sql").read_text()

class Entry:
    id: int
    slug: str
    body: str
    views: int
    content_md5_hash: str
    user_title: str
    user_description: str
    user_group: str
    #user_date_created: str
    #user_date_modified: str
    user_visibility: int
    user_draft: int

    def __init__(self, row):
        (
            self.id,
            self.slug,
            self.body,
            self.views,
            self.content_md5_hash,
            self.user_title,
            self.user_description,
            self.user_group,
            self.user_date_created,
            self.user_date_modified,
            self.user_visibility,
            self.user_draft,
        ) = row

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

    def get_entries(self):
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
            order by user_date_created desc
            """
        )

        return [ Entry(row) for row in cursor.fetchall() ]

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
