import React from 'react';
import ReactDOM from 'react-dom';
import Root from './root';
require('./scss/main.scss');


document.addEventListener('DOMContentLoaded', () => {
    const root = document.getElementById('root');

    ReactDOM.render(<Root />, root);
});