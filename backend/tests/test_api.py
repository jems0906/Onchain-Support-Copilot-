import importlib

import pytest
from fastapi.testclient import TestClient

import app.config as config
from app.main import app

client = TestClient(app)


def test_environment_config_supports_secret_and_bool_overrides(monkeypatch):
    monkeypatch.setenv('API_TOKEN', 'prod-token-123')
    monkeypatch.setenv('AUTH_REQUIRED', 'true')
    monkeypatch.setenv('RATE_LIMIT_PER_MINUTE', '200')
    monkeypatch.setenv('CORS_ALLOWED_ORIGINS', 'https://app.example.com, https://admin.example.com')

    importlib.reload(config)

    assert config.API_TOKEN == 'prod-token-123'
    assert config.AUTH_REQUIRED is True
    assert config.RATE_LIMIT_PER_MINUTE == 200
    assert config.get_allowed_origins() == ['https://app.example.com', 'https://admin.example.com']
    assert config.get_bool_env('AUTH_REQUIRED', False) is True

    importlib.reload(config)


def test_production_validation_requires_required_secrets(monkeypatch):
    monkeypatch.setenv('ENVIRONMENT', 'production')
    monkeypatch.setenv('AUTH_REQUIRED', 'true')
    monkeypatch.delenv('API_TOKEN', raising=False)
    monkeypatch.setenv('DATABASE_URL', 'postgresql+psycopg://user:pass@host:5432/support')
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)

    try:
        with pytest.raises(RuntimeError, match='API_TOKEN'):
            importlib.reload(config)
    finally:
        monkeypatch.delenv('ENVIRONMENT', raising=False)
        monkeypatch.setenv('AUTH_REQUIRED', 'false')
        monkeypatch.delenv('API_TOKEN', raising=False)
        monkeypatch.delenv('DATABASE_URL', raising=False)
        importlib.reload(config)


def test_health_endpoint_is_available():
    response = client.get('/api/health')
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'ok'
    assert payload['service'] == 'onchain-support-copilot'
    assert 'environment' in payload
    assert 'rate_limit_per_minute' in payload
    assert response.headers.get('X-Request-ID')


def test_rate_limit_blocks_excess_requests():
    original_limit = app.state.rate_limit_per_minute
    original_window = app.state.rate_limit_window_seconds
    app.state.rate_limit_per_minute = 2
    app.state.rate_limit_window_seconds = 60
    app.state.rate_limit_buckets.clear()

    try:
        for _ in range(2):
            response = client.get('/api/health')
            assert response.status_code == 200

        response = client.get('/api/health')
        assert response.status_code == 429
    finally:
        app.state.rate_limit_per_minute = original_limit
        app.state.rate_limit_window_seconds = original_window
        app.state.rate_limit_buckets.clear()


def test_protected_routes_require_api_token_when_enabled():
    original_required = getattr(app.state, 'auth_required', False)
    original_token = getattr(app.state, 'api_token', '')
    app.state.auth_required = True
    app.state.api_token = 'super-secret-token'

    try:
        response = client.post('/api/triage', json={
            'network': 'base',
            'error_message': 'RPC timeout while connecting',
            'tool_used': 'RPC endpoint',
        })
        assert response.status_code == 401

        response = client.post('/api/triage', json={
            'network': 'base',
            'error_message': 'RPC timeout while connecting',
            'tool_used': 'RPC endpoint',
        }, headers={'Authorization': 'Bearer super-secret-token'})
        assert response.status_code == 200
    finally:
        app.state.auth_required = original_required
        app.state.api_token = original_token


def test_cases_and_dashboard_are_available():
    assert client.get('/api/cases').status_code == 200
    dashboard = client.get('/api/dashboards/overview')
    assert dashboard.status_code == 200
    assert 'docs_gaps' in dashboard.json()


def test_triage_endpoint_returns_playbook_category():
    response = client.post('/api/triage', json={
        'network': 'base-sepolia',
        'error_message': 'RPC timeout while connecting',
        'tool_used': 'RPC endpoint',
    })
    assert response.status_code == 200
    assert response.json()['category'] == 'rpc-error'


def test_invalid_case_payload_is_rejected():
    response = client.post('/api/cases', json={
        'network': 'base',
        'transaction_hash': 'not-a-real-hash',
        'error_message': 'Transaction reverted',
        'tool_used': 'Hardhat',
    })
    assert response.status_code == 422


def test_invalid_rpc_payload_is_rejected():
    response = client.post('/api/rpc/balance', json={
        'network': 'base',
        'value': 'bad-value'
    })
    assert response.status_code == 422
