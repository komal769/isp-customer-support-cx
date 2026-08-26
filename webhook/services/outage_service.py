from typing import Dict


MOCK_OUTAGES = {
    "560001": {
        "outage": True,
        "area": "560001",
        "estimatedResolution": "18:30"
    },
    "160001": {
        "outage": False,
        "area": "160001",
        "estimatedResolution": None
    }
}


def check_outage(postal_code: str) -> Dict:
    postal_code = postal_code.strip()

    if not postal_code.isdigit() or len(postal_code) not in (5, 6):
        raise ValueError("Invalid postal code")

    return MOCK_OUTAGES.get(
        postal_code,
        {
            "outage": False,
            "area": postal_code,
            "estimatedResolution": None
        }
    )