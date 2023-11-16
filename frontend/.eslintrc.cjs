module.exports = {
  root: true,
  parser: "@typescript-eslint/parser",
  parserOptions: {
    sourceType: "module",
    ecmaVersion: 2020,
    project: ["./tsconfig.json"],
    extraFileExtensions: [".svelte"], // This is a required setting in `@typescript-eslint/parser` v4.24.0.
  },
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:svelte/recommended",
    "prettier", // should be last
  ],
  plugins: ["@typescript-eslint", "testing-library", "jest-dom"],
  ignorePatterns: ["node_modules/**", "*.cjs", "svelte.config.js"],
  overrides: [
    {
      files: ["*.svelte"],
      parser: "svelte-eslint-parser",
      parserOptions: {
        parser: "@typescript-eslint/parser",
      },
    },
  ],
  rules: {
    "svelte/no-at-html-tags": "off",
    "svelte/valid-compile": "off",
  },
  globals: {
    google: "readonly",
  },
  env: {
    browser: true,
    es2017: true,
    node: true,
  },
}
