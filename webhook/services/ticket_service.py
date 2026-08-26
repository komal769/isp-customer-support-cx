from typing import Dict


MOCK_TICKETS = {
    "INC-10291": {
        "ticketId": "INC-10291",
        "status": "IN_PROGRESS",
        "estimatedResolution": "2 hours"
    },
    "INC-10001": {
        "ticketId": "INC-10001",
        "status": "RESOLVED",
        "estimatedResolution": None
    }
}


def get_ticket_status(ticket_id: str) -> Dict:
    ticket_id = ticket_id.strip().upper()

    if not ticket_id.startswith("INC-"):
        raise ValueError("Invalid ticket ID")

    if ticket_id not in MOCK_TICKETS:
        return {
            "ticketId": ticket_id,
            "status": "NOT_FOUND",
            "estimatedResolution": None
        }

    return MOCK_TICKETS[ticket_id]