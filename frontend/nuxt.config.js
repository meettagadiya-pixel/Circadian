export default {
  target: 'server',
  head: {
    title: 'Circadian Intelligence',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    ],
    link: [
      { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
      { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: true },
      { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap' }
    ]
  },
  css: ['~/assets/css/main.css'],
  plugins: [
    { src: '~/plugins/user-store.js', mode: 'client' }
  ],
  buildModules: ['@nuxtjs/tailwindcss'],
  env: {
    // Backend API URL — set this in your deployment environment
    // Do NOT put user IDs or secrets here — they become public
    CIRCADIAN_API_URL: process.env.CIRCADIAN_API_URL || 'http://localhost:8000'
  },
  tailwindcss: {
    cssPath: '~/assets/css/main.css',
    configPath: 'tailwind.config.js'
  }
}