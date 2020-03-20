// webpack.config.js
const path = require("path");
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const BundleTracker = require("webpack-bundle-tracker");
const LiveReloadPlugin = require("webpack-livereload-plugin");

module.exports = {
  mode: 'development',
  entry: './frontend/src/main.js',
  output: {
    filename: "[name].js",
    path: path.resolve("./frontend/dist/"),
    publicPath: ""
  },
  resolve: {
    alias: {
      // 'vue$': isDev ? 'vue/dist/vue.runtime.js' : 'vue/dist/vue.runtime.min.js',
      '@': path.resolve(__dirname, './frontend/src'),
    },
    extensions: ['.js', '.vue'],
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
      {
        test: /\.scss$/,
        use: [
          'vue-style-loader',
          'css-loader',
          'sass-loader'
        ]
      },
      {
        test: /\.js$/,
        use: 'babel-loader'
      },
      {
        test: /\.js$/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"]
          }
        }
      },
      {
        test: /\.css$/,
        use: [
          'vue-style-loader',
          'css-loader'
        ]
      },
      {
        test: /\.(png|jpg|jpeg|gif|svg)$/,
        loader: "file-loader",
        options: {
          name: "[name].[ext]",
          emitFile: true,
          context: "",
          publicPath: "/static/img/",
          outputPath: "img/"
        }
      },
      {
        test: /\.(woff|woff2)$/,
        loader: "file-loader",
        options: {
          name: "[name].[ext]",
          emitFile: true,
          context: "",
          publicPath: "/static/fonts/",
          outputPath: "fonts/"
        }
      }
    ]
  },
  plugins: [
    new VueLoaderPlugin(),
    new BundleTracker({filename: "./webpack-stats.json"}),
    new LiveReloadPlugin({
      appendScriptTag: true
    })
  ]
};
