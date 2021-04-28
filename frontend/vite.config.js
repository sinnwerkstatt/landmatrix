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
      $utils: resolve("src/utils"),
      $static: resolve("src/static"),
    },
  },
  build: {
    target: "es2015",
    assetsDir: "static/assets",
  },
  server: {
    proxy: {
      "/api": "http://localhost:8000",
      "/graphql": "http://localhost:8000",
      "/wagtailapi": "http://localhost:8000",
      "/media": "http://localhost:8000",
      "/static": "http://localhost:8000",
    },
  },
});
