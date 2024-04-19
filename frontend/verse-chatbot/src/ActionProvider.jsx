// Adapted from react-chatbox-kit documentation (https://fredrikoseberg.github.io/react-chatbot-kit-docs/docs/)

import React from 'react';
import { getProfessorResponse, getProfessorRecommendation } from './verseAPI'
import { separateTextByNewline } from './textHelpers';
import { createChatBotMessage } from 'react-chatbot-kit';

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
    const [selectedCourse, setSelectedCourse] = React.useState("English Literature");
    const [messageHistory, setMessageHistory] = React.useState([]);
    const [recommendationCounter, setRecommendationCounter] = React.useState(0);

    const handleQuery = (query) => {
        setMessageHistory(prevMessages => [...prevMessages, query]);
        setRecommendationCounter(prevCount => prevCount + 1);

        getProfessorResponse(query, selectedCourse).then(output => {
            const response = separateTextByNewline(output);
            const answer = response[0];
            const answerMessage = createChatBotMessage(answer);

            // if a segue was not provided, do not overindex
            if (response.length === 3) {
                const segue = response[2];
                const segueMessage = createChatBotMessage(segue);

                setState((prev) => ({
                    ...prev,
                    messages: [...prev.messages, answerMessage, segueMessage],
                }));

                setMessageHistory(prevMessages => [...prevMessages, answer, segue]);

                if (recommendationCounter !== 0 && recommendationCounter % 2 === 0) {
                    const recommendationMessage = createChatBotMessage('Access a real-time recommendation based on our conversation', {
                        widget: 'recommendation'
                    });

                    setState((prev) => ({
                        ...prev,
                        messages: [...prev.messages, recommendationMessage],
                    }));
                }
            } else {
                setState((prev) => ({
                    ...prev,
                    messages: [...prev.messages, answerMessage],
                }));

                setMessageHistory(prevMessages => [...prevMessages, answer]);

                if (recommendationCounter !== 0 && recommendationCounter % 2 === 0) {
                    const recommendationMessage = createChatBotMessage('Access a real-time recommendation based on our conversation', {
                        widget: 'recommendation'
                    });

                    setState((prev) => ({
                        ...prev,
                        messages: [...prev.messages, recommendationMessage],
                    }));
                }

            }
        }).catch(error => {
            console.log("Error handling query: ", error)
        });
    };

    ///////////////

    const handleAmNovelCourse = () => {
        const message = createChatBotMessage("Let's focus on The American Novel Since 1945. What questions do you have?");

        setState((prev) => ({
            ...prev,
            messages: [...prev.messages, message],
        }));

        setMessageHistory(prevMessages => [...prevMessages, "Let's focus on The American Novel Since 1945. What questions do you have?"]);

        setSelectedCourse("The American Novel Since 1945");
    };

    const handleTheoryLitCourse = () => {
        const message = createChatBotMessage("Let's focus on Introduction to Theory of Literature. What questions do you have?");

        setState((prev) => ({
            ...prev,
            messages: [...prev.messages, message],
        }));

        setMessageHistory(prevMessages => [...prevMessages, "Let's focus on Introduction to Theory of Literature. What questions do you have?"]);

        setSelectedCourse("Introduction to Theory of Literature");
    };

    const handleMiltonCourse = () => {
        const message = createChatBotMessage("Let's focus on Milton. What questions do you have?");

        setState((prev) => ({
            ...prev,
            messages: [...prev.messages, message],
        }));

        setMessageHistory(prevMessages => [...prevMessages, "Let's focus on Milton. What questions do you have?"]);

        setSelectedCourse("Milton");
    };

    const handlePoetryCourse = () => {
        const message = createChatBotMessage("Let's focus on Modern Poetry. What questions do you have?");

        setState((prev) => ({
            ...prev,
            messages: [...prev.messages, message],
        }));

        setMessageHistory(prevMessages => [...prevMessages, "Let's focus on Modern Poetry. What questions do you have?"]);

        setSelectedCourse("Modern Poetry");
    };

    ///////////////

    const handleRecommendation = () => {
        getProfessorRecommendation(selectedCourse, messageHistory).then(recommendation => {
            const recommendationMessage = createChatBotMessage(recommendation);

            setState((prev) => ({
                ...prev,
                messages: [...prev.messages, recommendationMessage],
            }));

            setMessageHistory(prevMessages => [...prevMessages, recommendation]);
        }).catch(error => {
            console.log("Error handling recommendation retrieval: ", error)
        });
    };

    return (
        <div>
            {React.Children.map(children, (child) => {
                return React.cloneElement(child, {
                    actions: {
                        handleQuery,
                        handleAmNovelCourse,
                        handleTheoryLitCourse,
                        handleMiltonCourse,
                        handlePoetryCourse,
                        handleRecommendation,
                    },
                });
            })}
        </div>
    );
};

export default ActionProvider;