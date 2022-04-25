import adapter from "@sveltejs/adapter-node";
import { resolve } from "path";
import preprocess from "svelte-preprocess";
import { isoImport } from "vite-plugin-iso-import";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://github.com/sveltejs/svelte-preprocess
  // for more information about preprocessors
  preprocess: [
    preprocess({
      postcss: true,
    }),
  ],

  kit: {
    adapter: adapter(),
    vite: {
      plugins: [isoImport()],
      resolve: {
        alias: {
          $components: resolve("src/components"),
          $views: resolve("src/views"),
          // $static: resolve("static"),
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
          "/editor": "http://localhost:8000",
        },
      },
    },
  },
};

export default config;
