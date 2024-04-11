// Adapted from react-chatbox-kit documentation (https://fredrikoseberg.github.io/react-chatbot-kit-docs/docs/)

import React from "react";

import "./Recommendation.css";

const Recommendation = (props) => {
    const recommendationOptions = [
        {
            recommendation: 'Recommendation',
            handler: props.actionProvider.handleRecommendation,
            id: 1,
        },
    ];

    const buttonsMarkup = recommendationOptions.map((recommendationOption) => (
        <button key={recommendationOption.id} onClick={recommendationOption.handler} className="recommendation-option-button">
            {recommendationOption.recommendation}
        </button>
    ));

    return <div className="recommendation-options-container">{buttonsMarkup}</div>;
}

export default Recommendation;