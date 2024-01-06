import adapter from "@sveltejs/adapter-node"
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte"

/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://github.com/sveltejs/svelte-preprocess
  // for more information about preprocessors
  preprocess: [vitePreprocess({ postcss: true })],
  kit: {
    env: { dir: ".." },
    adapter: adapter(),
    alias: {
      $components: "src/components",
      $views: "src/views",
      $lib: "src/lib",
    },
  },
}

export default config
