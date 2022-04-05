const defaultTheme = require("tailwindcss/defaultTheme");

const config = {
  content: ["./src/**/*.{vue,html,js,ts}"],

  theme: {
    extend: {
      colors: {
        orange: {
          50: "hsl(32, 97%, 95%)",
          200: "hsl(32, 97%, 65%)",
          DEFAULT: "hsl(32, 97%, 55%)",
          600: "hsl(32, 97%, 45%)",
        },
        teal: {
          200: "hsl(179, 46%, 59%)",
          DEFAULT: "hsl(179, 46%, 49%)",
          600: "hsl(179, 46%, 39%)",
        },
        "lm-dark": "#4a4a4a",
        "lm-light": "#f9f9f9",
      },
    },
  },

  plugins: [],
};

module.exports = config;
