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
    "plugin:import/recommended",
    "plugin:import/typescript",
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
      rules: {
        "import/no-unresolved": [
          "error",
          {
            ignore: ["^\\$app/"],
          },
        ],
      },
    },
  ],
  settings: {
    "import/resolver": {
      typescript: true,
      node: true,
    },
    "import/parsers": {
      "@typescript-eslint/parser": [".ts"],
      espree: [".js", ".cjs", ".mjs"],
    },
  },
  rules: {
    "svelte/no-at-html-tags": "off",
    "svelte/valid-compile": "off",
    "import/no-named-as-default-member": "off",
    "import/order": [
      "warn",
      {
        groups: [
          "builtin", // Built-in imports (come from NodeJS native) go first
          "external", // <- External imports
          "internal", // <- Absolute imports
          ["sibling", "parent"], // <- Relative imports
          "unknown", // <- unknown
        ],
        pathGroups: [
          {
            pattern: "$app/**",
            group: "internal",
            position: "before",
          },
          {
            pattern: "$lib/**",
            group: "internal",
            position: "before",
          },
          {
            pattern: "$components/**",
            group: "internal",
            position: "before",
          },
        ],
        "newlines-between": "always",
        alphabetize: {
          caseInsensitive: true,
        },
      },
    ],
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
