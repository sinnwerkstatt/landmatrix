import { sveltekit } from "@sveltejs/kit/vite";
import { resolve } from "path";
import { defineConfig } from "vite";
import { isoImport } from "vite-plugin-iso-import";

export default defineConfig({
  plugins: [sveltekit(), isoImport()],
  resolve: {
    alias: {
      $components: resolve("src/components"),
      $views: resolve("src/views"),
    },
  },
  envDir: "..",
  test: {
    include: ["src/**/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}"],
    globals: true,
    environment: "jsdom",
  },
  optimizeDeps: { exclude: ["@urql/svelte"] },
  server: {
    port: 3000,
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
      "/editor": "http://localhost:8000",
    },
  },
});
