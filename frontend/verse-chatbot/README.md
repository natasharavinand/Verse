# Verse

*Verse* is an LLM-integrated software application enhanced with retrieval augmented generation designed for English literature pedagogy. Verse is enhanced with materials from Yale University's English Literature OpenCourseware Program ([link](https://oyc.yale.edu/english)).

-------------------

## Technical Overview

On the frontend, the UI uses:

- `JavaScript`, for client-side development
- `React`, a framework to build user interfaces
	- `react-chatbot-kit`, a React open-source package designed to create configurable chatbots. Documentation for this package, can be found [here](https://fredrikoseberg.github.io/react-chatbot-kit-docs/). 

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

*Note: The configuration instructions must be followed before running Verse.*

### Running Verse as a full-stack React application

To run Verse as a full-stack React application, follow three steps:

1.  `cd` to `api/`. Run the Verse API in debug mode locally with the following command:
	```
	flask --app verse --debug run
	```

	The application can also be run without the `--debug` flag, though changes in the source code will not be automatically integrated.

	You can additionally specify the host with the `--host` flag. By default, Flask serves locally on `http://127.0.0.1:5000`.

2. `cd` to `frontend/verse-chatbot`. Install any necessary dependencies with `npm install`.
3. Run the application with `npm start`. By default, React will locally serve the application on `http://localhost:3000`.
