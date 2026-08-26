# ISP Customer Support Assistant - Testing

## Test Cases

| Test ID | Scenario | Input / Steps | Expected Result | Status |
|---|---|---|---|---|
| TC01 | Connectivity Happy Path | Internet not working → One device → Follow troubleshooting → Yes | Issue resolved successfully | PASS |
| TC02 | Connectivity Escalation | Internet not working → Troubleshooting unsuccessful → No | Escalation response is provided | PASS |
| TC03 | Outage Check | Ask about outage → Enter postal code | Outage status is returned | PASS |
| TC04 | Ticket Status | Ask for ticket status → Enter ticket ID | Ticket status is returned | PASS |
| TC05 | Interruption Handling | Start connectivity troubleshooting → Ask about outage | Agent switches to outage journey | PASS |
| TC06 | No Match | Enter an unsupported request | Fallback response is triggered | PASS |
| TC07 | No Input | Do not provide input when expected | No-input handling is triggered | PASS |
| TC08 | Backend Webhook | Send POST request with supported webhook tag | Valid fulfillment response is returned | PASS |