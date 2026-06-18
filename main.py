import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app()

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
    port = int(os.getenv('PORT', 5001))  # Default to 5001 to avoid AirPlay conflict
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
