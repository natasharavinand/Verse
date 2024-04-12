// Adapted from react-chatbox-kit documentation (https://fredrikoseberg.github.io/react-chatbot-kit-docs/docs/)

import React from "react";

import "./CourseOptions.css";

const CourseOptions = (props) => {
    const courseOptions = [
        {
            course: 'The American Novel Since 1945',
            handler: props.actionProvider.handleAmNovelCourse,
            id: 1,
        },
        {
            course: 'Introduction to Theory of Literature',
            handler: props.actionProvider.handleTheoryLitCourse,
            id: 2,
        },
        {
            course: 'Milton',
            handler: props.actionProvider.handleMiltonCourse,
            id: 3,
        },
        {
            course: 'Modern Poetry',
            handler: props.actionProvider.handlePoetryCourse,
            id: 4,
        },
    ];

    const buttonsMarkup = courseOptions.map((courseOption) => (
        <button key={courseOption.id} onClick={courseOption.handler} className="course-option-button">
            {courseOption.course}
        </button>
    ));

    return <div className="course-options-container">{buttonsMarkup}</div>;
}

export default CourseOptions;