from my_flask_app import create_app
from dotenv import load_dotenv
import os
# IMPORT SECRETS

load_dotenv()
app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv('PORT'), host='0.0.0.0')