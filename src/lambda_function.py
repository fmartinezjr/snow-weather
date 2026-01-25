import json
import logging
import os
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

from api.weather import Config, SnowPeriod, check_snow_forecast

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class NotificationService:
    def __init__(self, email: str):
        self.email = email
        self.ses_client = boto3.client("ses")

    def _build_message(self, snow_periods: list[SnowPeriod]) -> str:
        message_parts = ["SNOW ALERT for Keystone, CO!\n"]

        for period in snow_periods:
            message_parts.append(f"{period.name}: {period.forecast}")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_parts.append(f"\nChecked at: {timestamp}")

        return "\n".join(message_parts)

    def send_alert(self, snow_periods: list[SnowPeriod]) -> bool:
        message = self._build_message(snow_periods)
        logger.info(f"Sending email to {self.email}")

        try:
            response = self.ses_client.send_email(
                Source="Snow Alert <panchventures@outlook.com>",
                Destination={"ToAddresses": ["franciscomj345@gmail.com"]},
                Message={
                    "Subject": {"Data": "SNOW ALERT for Keystone, CO!"},
                    "Body": {"Text": {"Data": message}}
                }
            )
            message_id = response["MessageId"]
            logger.info(f"Email sent successfully. MessageId: {message_id}")
            return True

        except ClientError as e:
            logger.error(f"AWS SES client error: {e}")
            return False
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False


def lambda_handler(event: dict, context: object) -> dict[str, str | int]:
    logger.info(f"Starting snow check at {datetime.now()}")

    config = Config()
    has_snow, snow_periods = check_snow_forecast(config)

    if not snow_periods and not has_snow:
        logger.info("No snow detected or failed to fetch weather data")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "No snow detected", "snow_periods": 0}),
        }

    if has_snow:
        logger.info(f"Snow detected! Found {len(snow_periods)} periods with snow")

        email = os.environ.get("EMAIL")
        if not email:
            logger.error("EMAIL environment variable not set")
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        "message": "Snow detected but alert failed (no email)",
                        "snow_periods": len(snow_periods),
                        "periods": [p.to_dict() for p in snow_periods],
                    }
                ),
            }

        notification_service = NotificationService(email)
        email_sent = notification_service.send_alert(snow_periods)

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": (
                        "Snow detected and alert sent"
                        if email_sent
                        else "Snow detected but alert failed"
                    ),
                    "snow_periods": len(snow_periods),
                    "periods": [p.to_dict() for p in snow_periods],
                }
            ),
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "No snow detected", "snow_periods": 0}),
    }
