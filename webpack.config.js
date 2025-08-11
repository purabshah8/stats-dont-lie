const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    mode: 'development',
    context: __dirname,
    entry: './frontend/index.jsx',
    output: {
        path: path.resolve(__dirname, 'assets', 'js'),
        filename: 'bundle.js',
        clean: true
    },
    resolve: {
        extensions: ['.js', '.jsx'],
        fallback: {
            "util": false,
            "crypto": false,
            "stream": false,
            "assert": false,
            "http": false,
            "https": false,
            "os": false,
            "url": false,
            "zlib": false
        }
    },
    plugins: [
        new BundleTracker({
            path: __dirname,
            filename: 'webpack-stats.json',
            publicPath: '/static/js/',
            logTime: true,
            relativePath: true
        }),
        new MiniCssExtractPlugin({
            filename: "../css/style.css"
        })
    ],
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        plugins: ["@babel/plugin-transform-async-to-generator"],
                        presets: [
                            ['@babel/preset-env', {
                                targets: {
                                    browsers: ['> 1%', 'last 2 versions']
                                }
                            }],
                            ['@babel/preset-react', {
                                runtime: 'automatic'
                            }]
                        ]
                    }
                }
            },
            {
                test: /\.(sa|sc|c)ss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'sass-loader'
                ]
            }
        ]
    },
    devtool: 'source-map'
};