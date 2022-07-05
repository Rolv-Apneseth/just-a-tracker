from pathlib import Path

from dotenv import load_dotenv
from flask_migrate import Migrate
from website import create_app, db

# CONSTANTS
FOLDER_PATH = Path(__file__).absolute().parent
ENV_PATH = FOLDER_PATH / ".env"

# Load environment variable(s)
load_dotenv(dotenv_path=ENV_PATH)

# Create flask app
app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run()
