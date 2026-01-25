# Snow Weather Alert

Python application that monitors weather forecasts and sends email alerts.

## Notifications

Currently using **AWS SES** for email notifications.

**SMS Support (WIP)**: Direct SMS via AWS SNS has poor deliverability with T-Mobile and other carriers. Future options:
- **10DLC Registration** - Standard approach for US SMS (~$15 setup, 1-2 weeks approval)
- **Toll-free Number** - Faster alternative (~$2/month, approved in hours/days)
- **AWS Pinpoint** - Better carrier support with dedicated numbers


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