import React from 'react';
import { ApolloClient, InMemoryCache, ApolloProvider, makeVar } from '@apollo/client';
import { BrowserRouter } from 'react-router-dom';
import App from './app';

// Create reactive variables for local state
export const navMenuIsActiveVar = makeVar(false);
export const themeVar = makeVar("default");

const Root = () => {
    const cache = new InMemoryCache({
        typePolicies: {
            Query: {
                fields: {
                    navMenuIsActive: {
                        read() {
                            return navMenuIsActiveVar();
                        }
                    },
                    theme: {
                        read() {
                            return themeVar();
                        }
                    }
                }
            }
        }
    });
    
    const client = new ApolloClient({
        uri: '/graphql/',
        cache
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