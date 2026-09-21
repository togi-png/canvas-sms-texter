import os
import json
import requests

from datetime import datetime, timedelta, timezone
from twilio.rest import Client
from openai import OpenAI


# =========================
# CONFIG
# =========================

CANVAS_URL = os.environ["CANVAS_URL"]
CANVAS_TOKEN = os.environ["CANVAS_TOKEN"]

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_FROM = os.environ["TWILIO_FROM"]

PHONE_TO = os.environ["PHONE_TO"]

canvas_headers = {
    "Authorization": f"Bearer {CANVAS_TOKEN}"
}


# =========================
# CANVAS FUNCTIONS
# =========================

def get_courses():
    url = f"{CANVAS_URL}/api/v1/courses"

    response = requests.get(
        url,
        headers=canvas_headers,
        params={
            "enrollment_state": "active"
        }
    )

    response.raise_for_status()

    return response.json()


def get_assignments(course_id):
    url = f"{CANVAS_URL}/api/v1/courses/{course_id}/assignments"

    response = requests.get(
        url,
        headers=canvas_headers,
        params={
            "include[]": ["submission"]
        }
    )

    response.raise_for_status()

    return response.json()


def is_incomplete(assignment):
    submission = assignment.get("submission", {})

    if submission.get("
