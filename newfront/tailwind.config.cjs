const defaultTheme = require("tailwindcss/defaultTheme");

const config = {
  content: ["./src/**/*.{html,js,svelte,ts}"],

  theme: {
    extend: {
      fontFamily: {
        sans: ["Open Sans", ...defaultTheme.fontFamily.sans],
      },
      colors: {
        orange: {
          DEFAULT: "#FC941F",
          50: "#FEEBD4",
          100: "#FEE1C0",
          200: "#FECE98",
          300: "#FDBA70",
          400: "#FDA747",
          500: "#FC941F",
          600: "#E07803",
          700: "#A95A02",
          800: "#713D02",
          900: "#3A1F01",
        },
        pelorous: {
          DEFAULT: "#44B7B6",
          50: "#C8EBEA",
          100: "#B9E5E5",
          200: "#9BDAD9",
          300: "#7ECFCE",
          400: "#60C4C3",
          500: "#44B7B6",
          600: "#358E8D",
          700: "#266565",
          800: "#163C3C",
          900: "#071313",
        },
        "lm-dark": "#4a4a4a",
        "lm-light": "#f9f9f9",
      },
      dropShadow: {
        marker: "3.5px 2.5px 0px rgba(0, 0, 0, 0.35)",
      },
    },
  },

  plugins: [],
};

module.exports = config;
