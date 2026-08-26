import logging

from fastapi import FastAPI, HTTPException

from webhook.models import DialogflowRequest
from webhook.services.outage_service import check_outage
from webhook.services.ticket_service import get_ticket_status


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ISP Customer Support Webhook",
    version="1.0.0"
)


def dialogflow_response(message: str, parameters: dict | None = None):
    response = {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [message]
                    }
                }
            ]
        }
    }

    if parameters:
        response["sessionInfo"] = {
            "parameters": parameters
        }

    return response


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/webhook")
def webhook(request: DialogflowRequest):

    tag = request.fulfillmentInfo.get("tag")

    parameters = request.sessionInfo.get(
        "parameters",
        {}
    )

    logger.info("Received webhook request. tag=%s", tag)

    try:

        if tag == "check_outage":

            postal_code = parameters.get("postal_code")

            if not postal_code:
                return dialogflow_response(
                    "Please provide your postal code so I can check for outages."
                )

            result = check_outage(str(postal_code))

            logger.info(
                "Outage lookup completed for area=%s",
                postal_code
            )

            if result["outage"]:

                message = (
                    f"There is currently an outage affecting "
                    f"{result['area']}. "
                    f"The estimated resolution time is "
                    f"{result['estimatedResolution']}."
                )

            else:

                message = (
                    f"I couldn't find an active outage for "
                    f"{result['area']}. "
                    "We can continue troubleshooting your connection."
                )

            return dialogflow_response(
                message,
                {
                    "outage_exists": result["outage"],
                    "outage_area": result["area"]
                }
            )

        elif tag == "check_ticket_status":

            ticket_id = parameters.get("ticket_id")

            if not ticket_id:
                return dialogflow_response(
                    "Please provide your ticket ID."
                )

            result = get_ticket_status(str(ticket_id))

            if result["status"] == "NOT_FOUND":

                return dialogflow_response(
                    f"I couldn't find ticket {result['ticketId']}. "
                    "Please check the ticket ID and try again."
                )

            message = (
                f"Ticket {result['ticketId']} is currently "
                f"{result['status'].replace('_', ' ').lower()}."
            )

            if result["estimatedResolution"]:
                message += (
                    f" The estimated resolution time is "
                    f"{result['estimatedResolution']}."
                )

            return dialogflow_response(message)

        else:

            logger.warning("Unknown webhook tag: %s", tag)

            raise HTTPException(
                status_code=400,
                detail="Unsupported webhook tag"
            )

    except ValueError as error:

        logger.warning("Validation error: %s", error)

        return dialogflow_response(
            "I couldn't process that information. "
            "Please check the value and try again."
        )

    except Exception:

        logger.exception("Unexpected webhook error")

        raise HTTPException(
            status_code=500,
            detail="Internal webhook error"
        )