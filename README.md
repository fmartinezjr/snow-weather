# Snow Weather Alert

Python application that monitors weather forecasts and sends SMS alerts


## Setup

Create a virtual environment and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev,test]"
```

## Test locally
```
python -m src.lambda_function
```