import pytest


@pytest.mark.parametrize(
    ["endpoint"], [["/rag/professorResponse"], ["/rag/professorRecommendation"]]
)
def test_rag_error_json(client, endpoint):
    """
    Ensures that each endpoint will ERROR if it is sent empty POSTed data.
    """
    with pytest.raises(ValueError):
        client.post(endpoint, data={})


@pytest.mark.parametrize("field", ["course", "query"])
def test_get_professor_response_missing_field(client, field, inputs_response):
    """
    Ensures that the /professorResponse route will ERROR if there is a missing field in the POSTed data.
    """
    del inputs_response[field]
    with pytest.raises(ValueError):
        client.post("/rag/professorResponse", json=inputs_response)
        
@pytest.mark.parametrize("field", ["course", "messages"])
def test_get_professor_recommendation_missing_field(client, field, inputs_recommendation):
    """
    Ensures that the /professorRecommendation route will ERROR if there is a missing field in the POSTed data.
    """
    del inputs_recommendation[field]
    with pytest.raises(ValueError):
        client.post("/rag/professorRecommendation", json=inputs_recommendation)
