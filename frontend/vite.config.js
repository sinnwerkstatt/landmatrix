import { resolve } from "path";
import { defineConfig } from "vite";
// import vue from "@vitejs/plugin-vue";
const { createVuePlugin } = require("vite-plugin-vue2");

export default defineConfig({
  plugins: [createVuePlugin(/*options*/)],

  resolve: {
    extensions: [".mjs", ".js", ".ts", ".jsx", ".tsx", ".json", ".vue"],
    alias: {
      $components: resolve("src/components"),
      $views: resolve("src/views"),
      $store: resolve("src/store"),
      $utils: resolve("src/utils"),
      $static: resolve("src/static"),
    },
  },
  css: {
    postcss: {
      plugins: [require("autoprefixer")],
    },
  },
  build: {
    target: "es2015",
    rollupOptions: {
      output: {
        // entryFileNames: `[name].js`,
        // chunkFileNames: `[name].js`,
        // assetFileNames: `[name].[ext]`,
        // chunkFileNames: ({ name }) =>
        //   name === "vendor" ? "vendor.js" : "[name]-[hash].js",
        // assetFileNames: ({ name }) =>
        //   name === "index.css" ? "index.css" : `[name].[hash].[ext]`,
      },
    },
  },
  server: {
    host: "0.0.0.0",
    proxy: {
      "/accounts": "http://localhost:8000",
      "/admin": "http://localhost:8000",
      "/api": "http://localhost:8000",
      "/cms": "http://localhost:8000",
      "/graphql": "http://localhost:8000",
      "/language": "http://localhost:8000",
      "/legacy": "http://localhost:8000",
      "/media": "http://localhost:8000",
      "/static": "http://localhost:8000",
      "/wagtailapi": "http://localhost:8000",
    },
  },
});
