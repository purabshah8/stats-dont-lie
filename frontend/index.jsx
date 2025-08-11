import React from 'react';
import { createRoot } from 'react-dom/client';
import Root from './root';
require('./scss/main.scss');


document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('root');
    const root = createRoot(container);
    
    root.render(<Root />);
});