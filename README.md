# Snow Weather Alert

Python application that monitors weather forecasts and sends SMS alerts


## Setup

Create a virtual environment and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .              # install project dependencies
pip install -e ".[dev]"       # install with dev dependencies
```

## Local Dev Checks
```
# Format code
black src/     

# Lint code     
ruff check src/  

# Type check   
mypy src/           
```

## Run Locally
```bash
python src/api/weather.py
```