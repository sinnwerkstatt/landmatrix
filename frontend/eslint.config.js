// @ts-check

import eslint from "@eslint/js"
import eslintConfigPrettier from "eslint-config-prettier"
import eslintPluginSvelte from "eslint-plugin-svelte"
import globals from "globals"
import svelteParser from "svelte-eslint-parser"
import tslint from "typescript-eslint"

// Seems to work without them ...
// import jestDom from "eslint-plugin-jest-dom"
// import testingLibrary from "eslint-plugin-testing-library"

export default tslint.config(
  eslint.configs.recommended,
  ...tslint.configs.recommended,
  ...eslintPluginSvelte.configs["flat/recommended"],
  eslintConfigPrettier,
  {
    files: ["**/*.svelte"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: { ...globals.node, ...globals.browser, google: "readonly" },
      parser: svelteParser,
      parserOptions: {
        parser: tslint.parser,
        extraFileExtensions: [".svelte"],
      },
    },
    rules: {
      "svelte/no-at-html-tags": "off",
      // "svelte/valid-compile": "off",
    },
  },
  {
    ignores: [
      "**/.svelte-kit",
      "**/build",
      "**/node_modules",
      "**/package",
      "eslint.config.js",
      "postcss.config.cjs",
      "tailwind.config.cjs",
    ],
  },
)
