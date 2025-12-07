/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        discord: {
          blurple: '#5865F2',
          green: '#57F287',
          yellow: '#FEE75C',
          fuchsia: '#EB459E',
          red: '#ED4245',
          white: '#FFFFFF',
          black: '#000000',
          dark: '#23272A',
          'not-quite-black': '#2C2F33',
          'dark-but-not-black': '#99AAB5',
        },
        primary: '#5865F2',
        secondary: '#57F287',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

