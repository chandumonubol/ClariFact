/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg_light: "#f8f9fa",
        bg_card: "#ffffff",
        bg_muted: "#e9ecef",
        text_primary: "#212529",
        text_secondary: "#6c757d",
        accent_primary: "#3b82f6",
        accent_secondary: "#10b981",
        accent_warning: "#f59e0b",
        accent_danger: "#ef4444",
        border: "#d1d5db",
      },
    },
  },
}