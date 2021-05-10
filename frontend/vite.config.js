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
    rollupOptions: {
      output: {
        entryFileNames: `[name].js`,
        chunkFileNames: `[name].js`,
        assetFileNames: `[name].[ext]`,
      },
    },
  },
  server: {
    proxy: {
      "/api": "http://localhost:8000",
      "/graphql": "http://localhost:8000",
      "/wagtailapi": "http://localhost:8000",
      "/media": "http://localhost:8000",
      "/static": "http://localhost:8000",
      "/legacy": "http://localhost:8000",
      "/cms": "http://localhost:8000",
    },
  },
});
