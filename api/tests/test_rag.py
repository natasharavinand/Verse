import pytest


@pytest.mark.parametrize(
    ["endpoint"], [["/rag/getStudentResponse"], ["/rag/getStudentRecommendation"]]
)
def test_rag_error_json(client, endpoint):
    """
    Ensures that each endpoint will ERROR if it is sent empty POSTed data.
    """
    with pytest.raises(ValueError):
        client.post(endpoint, data={})


@pytest.mark.parametrize("field", ["course", "query"])
def test_get_student_response_missing_field(client, field, inputs_response):
    """
    Ensures that the /getStudentResponse route will ERROR if there is a missing field in the POSTed data.
    """
    del inputs_response[field]
    with pytest.raises(ValueError):
        client.post("/rag/getStudentResponse", json=inputs_response)
        
@pytest.mark.parametrize("field", ["course", "messages"])
def test_get_student_recommendation_missing_field(client, field, inputs_recommendation):
    """
    Ensures that the /getStudentRecommendation route will ERROR if there is a missing field in the POSTed data.
    """
    del inputs_recommendation[field]
    with pytest.raises(ValueError):
        client.post("/rag/getStudentRecommendation", json=inputs_recommendation)