import os
import uvicorn
from main import app  # Import the FastAPI app from main.py

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")