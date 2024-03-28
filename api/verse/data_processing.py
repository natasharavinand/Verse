import re
import os
import zipfile
from bs4 import BeautifulSoup

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def unzip_file(zip_file_path, extracted_path):
    """
    unzip_file unzips a file from a given zip_file_path to a extracted_path.

    Args:
    zip_file_path (str): Path of file to unzip
    extracted_path(str): Path of file to unzip the contents to

    Returns:
    None

    Raises:
    None

    """

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extracted_path)


def convert_html_to_text(html_path):
    """
    convert_html_to_text converts the contents of html_path to plaintext.

    Args:
    html_path (str): Path of a given HTML file

    Returns:
    str: Plaintext of the file's contents

    Raises:
    None

    """

    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, "html.parser")
    return soup.get_text()


def extract_transcript_number(transcript_filename):
    """
    extract_transcript_number takes a transcript filename – in the format of transcript_01.html – and extracts the number
    of the transcript (ex. 1).

    Args:
    transcript_filename (str): Path of a given HTML file detailing a transcript, always in the format of transcript_##.html

    Returns:
    int: The number transcript the file describes

    Raises:
    None

    """

    return int(
        transcript_filename[
            transcript_filename.index(".") - 2 : transcript_filename.index(".")
        ]
    )


def get_cleaned_transcript_text(transcript_text):
    """
    get_cleaned_transcript_text takes in the text representation of a lecture and does some basic data cleaning
    to obtain the text in a processed format.

    Args:
    transcript_text (str): The text representation of a lecture (i.e., a transcript)

    Returns:
    str: The cleaned result of the passed in transcript_text

    Raises:
    None

    """

    # Remove dates and references to HTML
    date_pattern = re.compile(
        r"January|February|March|April|May|June|July|August|September|October|November|December"
    )
    transcript_text = re.sub(date_pattern, "", transcript_text)
    transcript_text = (
        transcript_text.replace("<< back", "")
        .replace("[end of transcript]", "")
        .replace("back to top", "")
    )
    transcript_text = re.sub(r"Lecture \d+ Transcript", "", transcript_text)

    # Remove course titles and professor names
    courses_to_professors = {
        "The American Novel Since 1945": "Professor Amy Hungerford",
        "Introduction to Theory of Literature": "Professor Paul Fry",
        "Modern Poetry": "Professor Langdon Hammer",
        "Milton": "Professor John Rogers",
    }

    for course in courses_to_professors:
        transcript_text = transcript_text.replace(course, "")
        transcript_text = transcript_text.replace(courses_to_professors[course], "")

    # Remove all non-alphabetized text before and after the lecture contents
    transcript_text = re.sub(r"^[^a-zA-Z]+", "", transcript_text)
    transcript_text = transcript_text.strip()

    return transcript_text


def process_course(course_num):
    """
    process_course executes the whole data processing pipeline. It extracts raw data into an extracted data
    path, and produces a cleaned file for each transcript for each lecture course in the ./data/processed directory.

    Args:
    course_num (int): The course number being processed.

    Returns:
    lecture_transcripts_map (dict[int:str]): This dictionary maps the lecture number to a text representation (transcript) of that lecture.

    Raises:
    None

    """

    # Define course paths given course number
    
    zipfile_path = os.path.join(BASEDIR, f"data/raw/engl{course_num}.zip")
    extracted_path = os.path.join(BASEDIR, f"data/extracted/engl{course_num}")

    if course_num == 220:
        extracted_transcripts_path = os.path.join(BASEDIR, "data/extracted/engl220/Milton/content/transcripts")
    else:
        extracted_transcripts_path = os.path.join(BASEDIR, f"data/extracted/engl{course_num}/ENGL{course_num} with 2012 Watermark/content/transcripts")

    # Unzip file contents into processed data directory
    unzip_file(zipfile_path, extracted_path)

    # Obtain plaintext of each lecture by generating transcript text
    lecture_transcripts_map = {}

    for file in os.listdir(extracted_transcripts_path):
        file_path = os.path.join(extracted_transcripts_path, file)
        transcript_pattern = re.compile(r"transcript\d+\.html", re.IGNORECASE)

        if os.path.isfile(file_path) and re.search(transcript_pattern, file):
            transcript_number = extract_transcript_number(file)
            transcript_text = convert_html_to_text(file_path)
            cleaned_transcript_text = get_cleaned_transcript_text(transcript_text)
            lecture_transcripts_map[transcript_number] = cleaned_transcript_text

    return lecture_transcripts_map


if __name__ == "__main__":
    course_numbers = [220, 291, 300, 310]
    
    processed_data_path = os.path.join(BASEDIR, "data/processed")
    if not os.path.exists(processed_data_path):
        os.makedirs(processed_data_path)

    for course_number in course_numbers:
        result = process_course(course_number)
        
        processed_course_path = os.path.join(BASEDIR, f"data/processed/{course_number}")
        if not os.path.exists(processed_course_path):
            os.makedirs(processed_course_path)

        for lecture_number, transcript in result.items():
            transcript_path = os.path.join(processed_course_path, f"lecture{lecture_number}.txt")
            with open(transcript_path, "w") as file:
                file.write(transcript)