# Sign Backend

## Setup
1. Create virtual environment:
   ```bash
   python3 -m venv venv
   ```
2. Activate virtual environment:
   ```bash
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run
1. Start the server (with reload):
   ```bash
   uvicorn main:app --reload
   ```
   
   To run on a specific host/port:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
