class Env:
  db_path: str

  def __init__(self):
    import os

    self.db_path = os.getenv("DATABASE_URL") or ".db.sqlite3"