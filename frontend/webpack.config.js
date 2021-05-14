// This file is only here for PyCharms path completion. Lets hope it'll support vite soon

const path = require("path");

module.exports = {
  resolve: {
    extensions: [".js", ".vue"],
    alias: {
      $components: path.resolve("src/components"),
      $views: path.resolve("src/views"),
      $store: path.resolve("src/store"),
      $utils: path.resolve("src/utils"),
      $static: path.resolve("src/static"),
    },
  },
};
