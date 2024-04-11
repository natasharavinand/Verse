import re
import verse.retrieval_augmented_generation as rag

from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

# create blueprint for RAG routes
bp = Blueprint("rag", __name__, url_prefix="/rag")


@bp.route("/professorResponse", methods=["OPTIONS", "POST"])
@cross_origin()
def professor_response():
    """
    professor_response takes in the user's course selection, a user query, and a list of previous responses and generates a response that imitates
    the tone and nature of a literature professor.

    Args:
        Expects JSON formatted data with the following fields:
        course (str): User's selected course
        query (str): The question or comment the user poses in the discussion
        previous_responses (Tuple[str]): A tuple of previous responses the model has generated

    Returns:
        If the request is JSON and contains the "course", "query", and "previous_responses" fields,
        it returns a JSON response with the model's response.
        Otherwise, it returns a 400 status code response.

    Raises:
        ValueError: If the request is not JSON formatted, one of the required fields are empty, or if the call to
        rag.get_llm_student_response() fails.
    """

    if not request.is_json:
        raise ValueError(
            {"error": "RESPONSE_ERROR", "message:": "Request must be JSON formatted."}
        )

    data = request.get_json()
    course = data.get("course")
    query = data.get("query")
    previous_responses = data.get("previous_responses")

    if not course:
        raise ValueError(
            {"error": "RESPONSE_ERROR", "message": "Course must be provided."}
        )

    if not query:
        raise ValueError(
            {"error": "RESPONSE_ERROR", "message": "Query must be provided."}
        )

    dangerous_characters_pattern = r"[;\'\\=<>/&]"
    query = re.sub(dangerous_characters_pattern, "", query)

    response = rag.get_professor_response(course, query, previous_responses)

    if not response:
        raise ValueError(
            {"error": "RESPONSE_ERROR", "message": "Error obtaining response."}
        )

    return jsonify(response), 200


@bp.route("/professorRecommendation", methods=["POST"])
@cross_origin()
def professor_recommendation():
    """
    professor_recommendation takes in the current course and all the messages from the suggestion and generates a context-dependent
    recommendation of prose to the student.

    Args:
        Expects JSON formatted data with the following fields:
        course (str): User's selected course
        messages (Tuple[str]): Tuple of the queries the user has submitted and the responses the model has provided

    Returns:
        If the request is JSON and contains the "course" and "messages" fields, it returns a JSON response with the model's response.
        Otherwise, it returns a 400 status code response.

    Raises:
        ValueError: If the request is not JSON formatted, one of the required fields are empty, or if the call to
        rag.get_student_recommendation() fails.
    """
    if not request.is_json:
        raise ValueError(
            {
                "error": "RECOMMENDATION_ERROR",
                "message:": "Request must be JSON formatted.",
            }
        )

    data = request.get_json()
    course = data.get("course")
    messages = data.get("messages")

    if not course:
        raise ValueError(
            {"error": "RECOMMENDATION_ERROR", "message": "Course must be provided."}
        )

    if not messages:
        raise ValueError(
            {"error": "RECOMMENDATION_ERROR", "message": "Messages must be provided."}
        )

    recommendation = rag.get_professor_recommendation(course, messages)

    if not recommendation:
        raise ValueError(
            {
                "error": "RECOMMENDATION_ERROR",
                "message": "Error obtaining recommendation.",
            }
        )

    return jsonify(recommendation), 200
