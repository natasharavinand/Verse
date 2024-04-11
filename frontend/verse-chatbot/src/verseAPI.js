const professorResponseEndpoint = 'http://127.0.0.1:5000/rag/professorResponse';
const professorRecommendationEndpoint = 'http://127.0.0.1:5000/rag/professorRecommendation';

export async function getProfessorResponse(query, selectedCourse) {
    const data = { course: selectedCourse, query: query };
    try {
        const response = await fetch(professorResponseEndpoint, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('Network response failed.');
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Fetch to API (/professorReesponse) errored: ', error);
        throw error;
    }
}

export async function getProfessorRecommendation(selectedCourse, messages) {
    const data = { course: selectedCourse, messages: messages };

    try {
        const response = await fetch(professorRecommendationEndpoint, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('Network response failed.');
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Fetch to API (/professorRecommendation) errored: ', error);
        throw error;
    }
}
