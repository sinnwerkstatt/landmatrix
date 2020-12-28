// webpack.config.js
require("core-js/stable");
require("regenerator-runtime/runtime");
// import "core-js/stable";
// import "regenerator-runtime/runtime";

const path = require("path");
const VueLoaderPlugin = require("vue-loader/lib/plugin");
const LiveReloadPlugin = require("webpack-livereload-plugin");

module.exports = {
  mode: "development",
  entry: ["./src/main.js"],
  output: {
    filename: "[name].js",
    path: path.resolve("./dist/"),
    publicPath: "",
    chunkFilename: "[id]-[chunkhash].js", // DO have Webpack hash chunk filename, see below
  },
  resolve: {
    modules: [path.resolve(__dirname, "src"), "node_modules"],
    extensions: [".js", ".vue"],
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: "vue-loader",
      },
      {
        test: /\.scss$/,
        use: ["vue-style-loader", "css-loader", "sass-loader"],
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,

        use: "babel-loader",
      },
      {
        test: /\.js$/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
          },
        },
      },
      {
        test: /\.css$/,
        use: ["vue-style-loader", "css-loader"],
      },
      {
        test: /\.(png|jpg|jpeg|gif|svg|ttf|woff|woff2|eot)$/i,
        use: {
          loader: "url-loader",
          options: {
            limit: 32 * 1024,
            fallback: "file-loader",
            emitFile: true,
            esModule: false,
            context: "",
            publicPath: "/static/assets/",
            outputPath: "assets/",
          },
        },
      },
    ],
  },
  devServer: {
    writeToDisk: true, // Write files to disk in dev mode, so Django can serve the assets
  },
  plugins: [
    new VueLoaderPlugin(),
    new LiveReloadPlugin({
      appendScriptTag: true,
    }),
  ],
};
