import pytest

from verse import create_app


@pytest.fixture
def app():
    app = create_app({"TESTING": True, "OPENAI_API_KEY": "testkey"})
    # yield
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


# valid test input for "/rag/getStudentResponse"
@pytest.fixture
def inputs_response():
    return {
        "course": "The Great American Novel Since 1945",
        "query": "Tell me about Toni Morrison.",
        "previous_responses": (),
    }
    
# valid test input for "/rag/getStudentRecommendation"
@pytest.fixture
def inputs_recommendation():
    return {
        "course": "The Great American Novel Since 1945",
        "messages": ("Sample query 1", "Sample response 1")
    }