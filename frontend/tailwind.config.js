module.exports = {
  mode: 'jit',
  purge: [
    './components/**/*.vue',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.js',
    './nuxt.config.js'
  ],
  theme: {
    extend: {
      colors: {
        'loop-navy': '#0A1628',
        'loop-dark': '#0F1F3D',
        'loop-card': '#162040',
        'loop-border': '#1E2F50',
        'loop-orange': '#FF9A09',
        'loop-orange-dim': '#FF9A0920',
        'loop-blue': '#0860FF',
        'loop-blue-dim': '#0860FF20',
        'loop-green': '#00C896',
        'loop-green-dim': '#00C89620',
        'loop-red': '#FF4757',
        'loop-red-dim': '#FF475720',
        'loop-yellow': '#FFD60A',
        'loop-text': '#E8EDF5',
        'loop-muted': '#6B7FA3',
      },
      fontFamily: {
        sans: ['DM Sans', 'sans-serif'],
        mono: ['DM Mono', 'monospace'],
      },
      boxShadow: {
        'card': '0 4px 24px rgba(0,0,0,0.25)',
        'glow-orange': '0 0 20px rgba(255,154,9,0.3)',
        'glow-blue': '0 0 20px rgba(8,96,255,0.3)',
        'glow-green': '0 0 20px rgba(0,200,150,0.3)',
        'glow-red': '0 0 20px rgba(255,71,87,0.3)',
      }
    }
  },
  plugins: []
}
