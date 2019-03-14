const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: './frontend/index.jsx',
    output: {
        path: path.resolve(__dirname, 'assets', 'js'),
        filename: 'bundle.js'
    },
    resolve: {
        extensions: ['.js', '.jsx', '*']
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
    ],
    rules: [
        {
            test: /\.jsx?$/,
            exclude: /(node_modules)/,
            use: {
                loader: 'babel-loader',
                query: {
                    presets: ['@babel/env', '@babel/react']
                }
            },
        }
    ],

};