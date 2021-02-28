from dotenv import load_dotenv
from pathlib import Path

from website import create_app


# CONSTANTS
FOLDER_PATH = Path(".")
ENV_PATH = FOLDER_PATH / ".env"

# Load environment variable(s)
load_dotenv(dotenv_path=ENV_PATH)

# Create flask app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
