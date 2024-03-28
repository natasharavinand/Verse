# Verse

*Verse* is an LLM-integrated software application enhanced with retrieval augmented generation designed for English literature pedagogy. Verse is enhanced with materials from Yale University's English Literature OpenCourseware Program ([link](https://oyc.yale.edu/english)).

-------------------
  
On the backend, this Verse is powered with a Flask API. The API uses:
  
-  `GPT-3.5-turbo`, OpenAI's fast, chat-based 3rd-generation LLM

-  `langchain`, a framework that helps software engineers develop applications with LLMs

-  `ChromaDB`, an open-source embedding database

-  `beautifulsoup4`, a web-scraping package to process and transform raw data from course materials into transcripts

The layout of the API was developed according to Flask [documentation](https://flask.palletsprojects.com/en/3.0.x/tutorial/).

The project uses `pytest` for testing.

## Installation Instructions


### Install the Verse API

1. Clone this repository using `HTTPS`, `SSH`, or the GitHub CLI.

2. Install `pip` according to system configuration.

3. [Optional] Create and activate a virtual environment to install requirements.

4.  `cd` into the `api/` directory. Then, run the following command:

	```
	pip install -e .
	```

	This command installs the `verse` package in editable mode.

## Configuration Instructions

### Configuring the Verse API

You need to configure two areas to run the Verse API.

#### Setting up OpenAI API Key

You need an OpenAI API key to use Verse. Add a `.env` file to the `api/` directory with your OpenAI API key, as indicated below:

```
OPENAI_API_KEY="YOURKEYHERE"
```

#### Generating ChromaDB database locally

The ChromaDB database is not stored on the Git repository due to space constraints. To generate the database locally, execute these two scripts in the `api/verse/` folder:

```
python3 data_processing.py
python3 vector_database.py
```

`data_processing.py` extracts and processes the raw data in `api/verse/data/raw` into the `api/verse/data/extracted` and `api/verse/data/processed` directories. 

`vector_database.py` uses the processed data to create a new ChromaDB database in `api/verse/` called `chroma/`. Inside `chroma/`, you will find a `sqlite3` database representing a ChromaDB.

## Running Verse

### Running Verse as a Streamlit application

To run the Streamlit demo of the Verse application, follow two steps:

1.  `cd` to `api/`. Run the Verse API in debug mode locally with the following command:
	```
	flask --app verse --debug run
	```

	The application can also be run without the `--debug` flag, though changes in the source code will not be automatically integrated.

	You can additionally specify the host with the `--host` flag. By default, Flask serves locally on `http://127.0.0.1:5000`.

2.  `cd` from `api/` to `api/verse/` and run the Streamlit app:

	```
	streamlit run verse_streamlit_app.py
	```

	By default, Streamlit serves locally on `http://localhost:8501`.

### Using the Verse API directly
You can call endpoints from the Verse API as well. 

Before you call these endpoints, ensure you are running the Flask server locally from the `api/` directory. You can run the API in debug mode using:

	
	flask --app verse --debug run
	
	
The application can also be run without the `--debug` flag, though changes in the source code will not be automatically integrated.

### Endpoints Available in the API

You can view the implementation of each endpoint in `api/verse/retrieval_augmented_generation.py`. 

The following endpoints are provided in the Verse API and are implemented in `api/verse/routes/rag.py`:

1. `rag/professorResponse`: `rag/professorResponse` takes in the user's course selection, a user query, and a tuple of previous LLM responses and generates a response that imitates the tone and nature of a literature professor.
2. `rag/professorRecommendation`: `rag/professorRecommendation` takes in the user's course selection and a tuple of the messages in the session (both queries posed by user as well as responses from the model) and generates a dynamic prose recommendation for the user.
