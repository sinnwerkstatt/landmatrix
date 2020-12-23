// webpack.config.js
// require("@babel/polyfill");
import "core-js/stable";
import "regenerator-runtime/runtime";

const path = require("path");
const VueLoaderPlugin = require("vue-loader/lib/plugin");
// const BundleTracker = require("webpack-bundle-tracker");
const LiveReloadPlugin = require("webpack-livereload-plugin");

module.exports = {
  mode: "development",
  entry: ["@babel/polyfill", "./src/main.js"],
  output: {
    filename: "[name].js",
    path: path.resolve("./dist/"),
    publicPath: "",
  },
  resolve: {
    modules: [path.resolve(__dirname, "src"), "node_modules"],
    extensions: [".js", ".vue", ".scss"],
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
  plugins: [
    new VueLoaderPlugin(),
    // new BundleTracker({ filename: "./webpack-stats.json" }),
    new LiveReloadPlugin({
      appendScriptTag: true,
    }),
  ],
};
