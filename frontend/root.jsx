import React from 'react';
import ApolloClient from 'apollo-boost';
import { ApolloProvider } from "react-apollo";
import { InMemoryCache } from "apollo-cache-inmemory";
import { BrowserRouter } from 'react-router-dom';
import App from './app';

const Root = () => {
    const cache = new InMemoryCache();
    const client = new ApolloClient({
        cache,
        clientState: {
            defaults: {
                navMenuIsActive: false,
            },
            resolvers: {},
            typeDefs: `
            extend type Query {
                navMenuIsActive: Boolean,
                theme: String
            }
            `
        }
    });
    cache.writeData({
        data: {
            navMenuIsActive: false,
            theme: "default",
        },
    });
    return (
        <ApolloProvider client={client}>
            <BrowserRouter>
                <App />
            </BrowserRouter>
        </ApolloProvider>
    );
};



export default Root;