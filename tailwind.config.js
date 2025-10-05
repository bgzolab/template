import typography from '@tailwindcss/typography';

export default {
  content: [
    "./src/**/*.{astro,js,ts,vue}",
    "./public/**/*.html"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    typography,
  ],
}