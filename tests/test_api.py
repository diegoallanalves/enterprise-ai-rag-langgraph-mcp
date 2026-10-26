from fastapi.testclient import TestClient
from app.api import app
from app.knowledge import retrieve

client = TestClient(app)

def test_health():
    assert client.get('/health').json() == {'status': 'ok'}

def test_grounded_answer():
    result = client.post('/ask', json={'question': 'What is data quality?'}).json()
    assert result['sources']
    assert 'data_quality' in result['answer']

def test_abstains_when_no_evidence():
    result = client.post('/ask', json={'question': 'zxqv blorp'}).json()
    assert result['sources'] == []
    assert 'don\'t have supporting evidence' in result['answer']

def test_retrieval():
    assert retrieve('incident SLA')[0].source == 'sla'
