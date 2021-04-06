import { resolve } from "path";
import { defineConfig } from "vite";
// import vue from "@vitejs/plugin-vue";
const { createVuePlugin } = require("vite-plugin-vue2");

export default defineConfig({
  plugins: [createVuePlugin(/*options*/)],

  resolve: {
    extensions: [".js", ".vue"],
    alias: {
      $components: resolve("src/components"),
      $views: resolve("src/views"),
      $store: resolve("src/store"),
      static: resolve("src/static"),
      $utils: resolve("src/utils"),
    },
  },
});
