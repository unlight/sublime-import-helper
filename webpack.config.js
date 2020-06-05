const webpack = require('webpack');
const path = require('path');

const config = {
    entry: 'import-adjutor/cli.js',
    output: {
        path: process.cwd(),
        filename: 'backend_run.js',
    },
    target: 'node',
    mode: 'development',
    devtool: false,
    module: {
        rules: [],
    },
    resolve: {
        extensions: ['.js'],
    },
};

module.exports = config;
