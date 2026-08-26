# ISP Customer Support – Dialogflow CX & FastAPI Webhook

An end-to-end Conversational AI assistant for Internet Service Provider (ISP) customer support, built using **Dialogflow CX** and a modular **FastAPI** Python backend.

The assistant supports three primary customer journeys:

- Internet connectivity troubleshooting
- Outage checking
- Ticket status lookup

---

## 1. Deliverables & Project Structure

```text
isp-customer-support-cx/
│
├── README.md
│
├── architecture/
│   └── conversation_flow.png
│
├── dialogflow/
│   └── agent_export.zip
│
└── webhook/
    ├── app.py
    ├── models.py
    ├── requirements.txt
    │
    ├── services/
    │   ├── outage_service.py
    │   └── ticket_service.py
    │
    └── tests/
        └── test_webhook.py
```

### Project Components

| Component | Description |
|---|---|
| `architecture/` | Contains the conversation flow diagram |
| `dialogflow/` | Contains the exported Dialogflow CX agent configuration |
| `webhook/app.py` | Webhook entry point and request dispatcher |
| `webhook/models.py` | Request and response data models |
| `webhook/services/outage_service.py` | Outage lookup and input validation logic |
| `webhook/services/ticket_service.py` | Ticket status lookup logic |
| `webhook/tests/` | Unit and integration tests |

---

## 2. Prerequisites

Before running the project, ensure you have:

- Python 3.10+
- A Google Cloud project with Dialogflow CX enabled
- `ngrok` for exposing the local webhook during development
- Required Python dependencies

---

## 3. How to Run the Webhook

### Activate the Virtual Environment

**PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r webhook/requirements.txt
```

### Start the FastAPI Webhook Server

```bash
python -m uvicorn webhook.app:app --reload --port 8000
```

The webhook will start locally at:

`http://localhost:8000`

---

## 4. Expose the Local Webhook

To allow Dialogflow CX to access the locally running FastAPI application, expose it using ngrok:

```bash
ngrok http 8000
```

Copy the generated HTTPS forwarding URL and configure it as the webhook endpoint in Dialogflow CX.

Example:

```text
https://your-ngrok-url.ngrok-free.app/webhook
```

---

## 5. Running Tests

Execute the unit and integration tests using Pytest:

```bash
pytest webhook/tests/
```

---

## 6. Architectural Decisions

### Modular Service Architecture

The backend follows a modular architecture that separates Dialogflow CX webhook request handling from domain-specific business logic.

- `app.py` handles webhook requests and response dispatching.
- `outage_service.py` handles outage lookup and validation logic.
- `ticket_service.py` handles ticket status lookup.

This separation improves maintainability, testability, and scalability.

### Multi-Tier Fallback Handling

The conversational flows implement a three-level fallback strategy using:

- `sys.no-match-1`
- `sys.no-match-2`
- `sys.no-match-3`

and:

- `sys.no-input-1`
- `sys.no-input-2`
- `sys.no-input-3`

This allows the assistant to progressively recover from unrecognized or missing user input before escalating or ending the conversation.

### Resilient Webhook Recovery

Webhook failures are handled using:

- `sys.webhook-error` events
- `$session.params.webhook_status` conditional routes

This prevents the conversation from reaching dead-end states when backend services are temporarily unavailable.

---

## 7. Interruption & Resumption Approach

### Global Intent Routing

Core user intents, including:

- `intent.check_outage`
- `intent.check_ticket`
- `intent.troubleshoot`

are configured through global routing to allow users to switch between supported journeys during a conversation.

For example, a user troubleshooting an internet issue can ask about an outage without manually restarting the conversation.

### Session Parameter Retention

Collected parameters are retained in `$session.params` when the user transitions between flows.

This allows the assistant to preserve relevant context and resume a previous task without unnecessarily asking the user for the same information again.

---

## 8. Production Considerations

### Monitoring

If deployed to production, the following metrics would be monitored:

- **Webhook latency and failures:** Monitor p95/p99 response latency, timeout rates, and HTTP 5xx errors.
- **No-match rate:** Track the frequency of `sys.no-match` events to identify missing intents or insufficient training phrases.
- **Conversation abandonment:** Identify where users leave conversations before completing their task, including repeated no-input events.
- **Successful task completion:** Track successful completion of key customer journeys such as connectivity troubleshooting, outage checks, and ticket status lookup.
- **Escalation rate:** Monitor how frequently users are transferred to human support to identify areas where the assistant requires improvement.

### API Credentials and Secrets

API keys, tokens, and other credentials should not be hardcoded in the source code.

In production, secrets should be securely stored and retrieved dynamically using a service such as **Google Cloud Secret Manager**.

### Sensitive Customer Information

Only the minimum customer information required to complete a task should be collected.

Sensitive information should be masked where possible and should not be unnecessarily exposed in responses, logs, or analytics systems.

### Webhook Authentication

The webhook endpoint should be protected using authentication and authorization mechanisms such as:

- Bearer tokens
- Service-to-service authentication
- IAM-based authentication
- Request validation

### Logging of Customer Data

Logs should avoid storing sensitive customer information.

Where customer identifiers or other sensitive fields are required for troubleshooting, values should be masked or sanitized, and access to logs should be restricted to authorized personnel.

---

## 9. Known Limitations

### In-Memory Data Store

The current implementation uses mock dictionaries within the service layer instead of persistent databases or external ISP APIs.

In a production implementation, these services would connect to secure backend systems or APIs.

### Local Webhook Exposure

The current development setup uses ngrok to expose the local FastAPI webhook.

In production, the webhook would be deployed to a managed environment such as Cloud Run or another secure hosting platform.

### Simulated Channels

Voice and telephony interactions are currently evaluated using standard text-based Dialogflow CX requests.

A production deployment would require integration with the appropriate telephony or voice platform.

---

## Architecture

The assistant is organized around three primary customer journeys:

```text
                         ┌─────────────────────┐
                         │   Customer Message  │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │ Dialogflow CX Agent │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
    ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
    │ Connectivity    │   │  Outage Check   │   │  Ticket Status  │
    │ Troubleshooting │   │                 │   │                 │
    └────────┬────────┘   └────────┬────────┘   └────────┬────────┘
             │                     │                     │
             └─────────────────────┼─────────────────────┘
                                   │
                        ┌──────────▼──────────┐
                        │  FastAPI Webhook    │
                        └──────────┬──────────┘
                                   │
                     ┌─────────────┴─────────────┐
                     │                           │
                     ▼                           ▼
              Outage Service               Ticket Service
```

---

## Future Improvements

Potential improvements include:

- Integration with real ISP backend APIs
- Persistent database integration
- Deployment to Google Cloud Run
- Enhanced analytics and monitoring
- Authentication using managed cloud identity services
- Additional multilingual and voice support