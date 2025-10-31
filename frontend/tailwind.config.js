/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f2f6ff",
          500: "#1f4fb2",
          600: "#153f8f"
        },
        accent: "#f19c1a"
      }
    }
  },
  plugins: [require("@tailwindcss/forms")]
};
