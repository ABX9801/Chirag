import uvicorn
from app.main import app
import sys

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)