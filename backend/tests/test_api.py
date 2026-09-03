from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


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
