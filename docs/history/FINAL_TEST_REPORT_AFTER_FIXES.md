C:\Users\jimmy\AppData\Roaming\Python\Python314\site-packages\fastapi\_compat\v1.py:72: UserWarning: Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.
  from pydantic.v1 import BaseConfig as BaseConfig  # type: ignore[assignment]
AWS Secrets Manager not available, using environment variables
{"timestamp": "2025-11-03T12:32:45.971286Z", "level": "INFO", "logger": "app.main", "message": "Tenant context middleware enabled", "module": "main", "function": "_add_middleware", "line": 263, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:45.971449Z", "level": "INFO", "logger": "app.main", "message": "Trusted host middleware enabled with secure validation", "module": "main", "function": "_add_middleware", "line": 325, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:46.055667Z", "level": "INFO", "logger": "app.main", "message": "FastAPI application created successfully", "module": "main", "function": "create_app", "line": 237, "taskName": null, "correlation_id": null}
================================================================================
COMPREHENSIVE ENDPOINT TESTING SUITE
================================================================================
Started: 2025-11-03T07:32:46.631942

Testing Health Endpoints...
{"timestamp": "2025-11-03T12:32:46.650157Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/ \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:46.657235Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/health \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:46.662179Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/health/live \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:46.670314Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/health/ready \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.528249Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/health/comprehensive \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.532215Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/health/circuit-breakers \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.534658Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/health/configuration \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.543380Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/metrics \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
Testing Authentication Endpoints...
{"timestamp": "2025-11-03T12:32:53.546389Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: POST http://localhost:8000/api/v1/auth/login \"HTTP/1.1 422 Unprocessable Entity\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.548891Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: POST http://localhost:8000/api/v1/auth/register \"HTTP/1.1 422 Unprocessable Entity\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.551947Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: POST http://localhost:8000/api/v1/auth/logout \"HTTP/1.1 403 Forbidden\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.555726Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: POST http://localhost:8000/api/v1/auth/refresh \"HTTP/1.1 422 Unprocessable Entity\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.618238Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: POST http://localhost:8000/api/v1/auth/password-reset \"HTTP/1.1 500 Internal Server Error\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.626670Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/auth/me \"HTTP/1.1 403 Forbidden\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
Testing User Endpoints...
{"timestamp": "2025-11-03T12:32:53.628917Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/users/me \"HTTP/1.1 401 Unauthorized\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.631586Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/users/ \"HTTP/1.1 403 Forbidden\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.633586Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/users/123 \"HTTP/1.1 403 Forbidden\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
Testing Posts Endpoints...
{"timestamp": "2025-11-03T12:32:53.643240Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/posts/ \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.651857Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/posts/99999 \"HTTP/1.1 404 Not Found\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.698070Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: POST http://localhost:8000/api/v1/posts/ \"HTTP/1.1 401 Unauthorized\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
Testing Guard Service Endpoints...
{"timestamp": "2025-11-03T12:32:53.764762Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: POST http://localhost:8000/api/v1/guards/process \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.768239Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/guards/status \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.772076Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/guards/health \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.774782Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/guards/services \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
Testing Subscription Endpoints...
{"timestamp": "2025-11-03T12:32:53.780365Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/subscriptions/tiers \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.789952Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/subscriptions/current \"HTTP/1.1 500 Internal Server Error\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.803270Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: POST http://localhost:8000/api/v1/subscriptions/checkout \"HTTP/1.1 500 Internal Server Error\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
Testing Organization Endpoints...
{"timestamp": "2025-11-03T12:32:53.821798Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/organizations/current \"HTTP/1.1 500 Internal Server Error\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.854288Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/organizations/members \"HTTP/1.1 500 Internal Server Error\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
Testing Legal Endpoints...
{"timestamp": "2025-11-03T12:32:53.860232Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/legal/terms-of-service \"HTTP/1.1 404 Not Found\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.862819Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/legal/privacy-policy \"HTTP/1.1 404 Not Found\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.865184Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/legal/cookie-policy \"HTTP/1.1 404 Not Found\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
Testing Analytics Endpoints...
{"timestamp": "2025-11-03T12:32:53.880180Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/analytics/benefits/overview \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.903206Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/analytics/benefits/detailed \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.907992Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/analytics/performance/dashboard \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
Testing File Upload Endpoints...
{"timestamp": "2025-11-03T12:32:53.914015Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/upload/health \"HTTP/1.1 200 OK\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}
{"timestamp": "2025-11-03T12:32:53.918487Z", "level": "INFO", "logger": "httpx", "message": "HTTP Request: GET http://localhost:8000/api/v1/upload/list \"HTTP/1.1 401 Unauthorized\"", "module": "_client", "function": "_send_single_request", "line": 1025, "taskName": null, "correlation_id": null}

================================================================================
TEST SUMMARY
================================================================================
Total Tests: 37
Passed: 31 [OK]
Failed: 6 [FAIL]
Success Rate: 83.8%

Failed Tests:
  [FAIL] POST /api/v1/auth/login
     Expected: 400, Got: 422
  [FAIL] POST /api/v1/auth/logout
     Expected: 401, Got: 403
  [FAIL] POST /api/v1/auth/refresh
     Expected: 400, Got: 422
  [FAIL] GET /api/v1/auth/me
     Expected: 401, Got: 403
  [FAIL] GET /api/v1/users/
     Expected: 401, Got: 403
  [FAIL] GET /api/v1/users/123
     Expected: 401, Got: 403

Detailed report saved to: test_results_comprehensive.json
