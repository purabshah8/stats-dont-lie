import React from 'react';
import ApolloClient from 'apollo-boost';
import { ApolloProvider } from "react-apollo";
import { BrowserRouter } from 'react-router-dom';
import App from './app';

const Root = () => {
    const client = new ApolloClient();

    return (
        <ApolloProvider client={client}>
            <BrowserRouter>
                <App />
            </BrowserRouter>
        </ApolloProvider>
    );
};



export default Root;