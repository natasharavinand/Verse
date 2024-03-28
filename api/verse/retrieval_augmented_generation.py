import os

from flask import current_app, g

from langchain.vectorstores.chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def get_global_llm():
    """
    get_global_llm generates a new instance of an OpenAI LLM object if it has not been created yet and adds it to the Flask global
    variable set.

    Args:
    None

    Returns:
    llm (ChatOpenAI): Object representing an LLM. Can be exchanged for another model.

    Raises:
    None
    """

    if "llm" not in g:
        g.llm = ChatOpenAI(
            openai_api_key=current_app.config["OPENAI_API_KEY"],
            model_name="gpt-3.5-turbo-1106",
            temperature=0.9,
        )
    return g.llm


def get_student_response(course, query, previous_responses):
    """get_student_response takes in the user's course selection, a user query, and a list of previous responses and generates a response that imitates
    the tone and nature of a literature professor.

    Args:
    course (str): User's selected course
    query (str): The question or comment the user poses in the discussion
    previous_responses (Tuple[str]): A list of previous responses the model has generated

    Returns:
    str: The response the model generates

    Raises:
    None

    """

    llm = get_global_llm()

    prompt_template = """
    You are an English literature professor leading a seminar with one student on {course}. Your responses should be engaging, authoritative, yet humble. Omit 
    responses like – "can I help you with anything else?" – and instead assume the role of an academic mentor.
    ------------------
    
    If the question requires external information, answer the question based on the following context:

    {context}

    ------------------
        
    Answer questions in a manner than assumes the user is either starting or in the middle of a dialogue with you. In order to help, use the following previous responses to understand 
    where in the conversation you are:

    {previous_responses} 

    ------------------

    Now, answer the following question, incorporating a significant amount of the context and previous responses. Here is the query: {query}
    
    """

    chroma_path = os.path.join(BASEDIR, "chroma")

    chromaDB_retriever = Chroma(
        persist_directory=chroma_path,
        collection_name="transcripts",
        embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"),
    ).as_retriever()
    documents = chromaDB_retriever.get_relevant_documents(query)
    context = "\n".join([doc.page_content for doc in documents])

    previous_responses = "\n".join(previous_responses)

    prompt_template = PromptTemplate(
        template=prompt_template,
        input_variables=["course", "context", "previous_responses", "query"],
    )
    answer_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="answer")

    overall_chain = SequentialChain(
        input_variables=["course", "context", "previous_responses", "query"],
        output_variables=["answer"],
        chains=[answer_chain],
    )

    response = overall_chain.invoke(
        {
            "course": course,
            "context": context,
            "previous_responses": previous_responses,
            "query": query,
        }
    )

    # if the result of the LLM call is incomplete, defer to the last complete sentence
    if response["answer"][-1] != ".":
        sentences = response["answer"].split(".")[:-1]
        response_to_user = ".".join(sentences) + "."
    else:
        response_to_user = response["answer"]

    if response_to_user[-1] != "?":
        segue_template = """
        You are a professor of literature teaching {course}. You have just answered a question posed by a student 
        and would like to segue the discussion via another interesting question or comment. 
    
        ------------------
        
        For context, you can refer to the original student question: {query} 
        
        ------------------
        
        You will be given the statement you made here: {statement}
        
        ------------------
        
        Now, generate the leading question or comment to the student.
        
        """

        segue_response_template = PromptTemplate(
            template=segue_template, input_variables=["course", "statement", "query"]
        )
        segue_chain = LLMChain(
            llm=llm, prompt=segue_response_template, output_key="answer"
        )

        segue_response_chain = SequentialChain(
            input_variables=["course", "statement", "query"],
            output_variables=["answer"],
            chains=[segue_chain],
        )

        segue = segue_response_chain.invoke(
            {"course": course, "statement": response["answer"], "query": query}
        )
        response_to_user += "\n\n" + segue["answer"].strip()

    return response_to_user


def get_student_recommendation(course, messages):
    """get_student_recommendation takes in the user's course selection and a list of the messages in the sent (both queries posed by
    user as well as responses from the model) and generates a text recommendation for the user.

    Args:
    course (str): User's selected course
    messages (List[str]): List of the queries the user has submitted and the responses the model has provided

    Returns:
    str: The recommendation the model generates

    Raises:
    None

    """

    llm = get_global_llm()

    recommendation_template = """
    You are a professor of literature teaching {course}. You have just had a session with a student in a 
    seminar and want to recommend they read another novel or work of poetry.

    ------------------
    
    For context, you can refer to the message history: {messages} 
    
    ------------------
    
    Now, generate the text you would recommend as well as some reasoning for why. If the student had any particular doubts or interest
    about something during the session, include this in your reasoning. Make this a short-form response of no more than a few sentences.
    """

    recommendation_response_template = PromptTemplate(
        template=recommendation_template, input_variables=["course", "messages"]
    )
    recommendation_chain = LLMChain(
        llm=llm, prompt=recommendation_response_template, output_key="recommendation"
    )

    recommendation_response_chain = SequentialChain(
        input_variables=["course", "messages"],
        output_variables=["recommendation"],
        chains=[recommendation_chain],
    )

    response = recommendation_response_chain.invoke(
        {"course": course, "messages": messages}
    )
    return response["recommendation"]