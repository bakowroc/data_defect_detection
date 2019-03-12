var path = require("path");

var config = {

    /* The entry point of the application. Webpack uses this information to 
    create the dependency tree which is used to bundle the scripts.*/
    entry: ["./src/index.tsx"],

    /* This information is used to give the name of the bundled file and the 
    location of the bundled file. */
    output: {
        path: path.resolve(__dirname, "build"),
        publicPath: "/build/",
        filename: "bundle.js"
    },

    /*  The extensions which will be imported or required in the application
    scripts. */
    resolve: {
        extensions: [".ts", ".tsx", ".js"]
    },
    devServer: {
        proxy: {
            '/api/**': {
                target: 'http://localhost:8000',
                pathRewrite: {'^/api' : ''}
            }
        }
    },

    module: {
        rules: [
          {
            enforce: 'pre',
            test: /\.tsx?$/,
            use: "source-map-loader",
            exclude: /node_modules/
        }, {
            test: /\.tsx?$/,
            loader: "ts-loader",
            exclude: /node_modules/
        }, {
            test: /\.css$/,
            use: ['style-loader', 'css-loader']
        }]
    },
    devtool: 'inline-source-map'
};

module.exports = config;