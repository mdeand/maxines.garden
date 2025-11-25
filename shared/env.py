class Env:
  db_path: str
  deployment_mode: str

  def __init__(self):
    import os

    self.db_path = os.getenv("DATABASE_URL") or ".db.sqlite3"
    self.deployment_mode = os.getenv("DEPLOYMENT_MODE") or "Debug"