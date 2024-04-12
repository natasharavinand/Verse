// Adapted from react-chatbox-kit documentation (https://fredrikoseberg.github.io/react-chatbot-kit-docs/docs/)

import React from 'react';

const MessageParser = ({ children, actions }) => {
    const parse = (message) => {
        actions.handleQuery(message);
    };

    return (
        <div>
            {React.Children.map(children, (child) => {
                return React.cloneElement(child, {
                    parse: parse,
                    actions,
                });
            })}
        </div>
    );
};

export default MessageParser;