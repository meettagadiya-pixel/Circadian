<template>
  <div class="flex h-screen overflow-hidden" style="background:#0A1628">

    <!-- Sidebar -->
    <aside class="w-60 flex-shrink-0 flex flex-col border-r" style="background:#0F1F3D; border-color:#1E2F50">

      <!-- Logo -->
      <div class="px-5 py-5 border-b" style="border-color:#1E2F50">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg flex items-center justify-center" style="background: linear-gradient(135deg, #FF9A09, #FF6B00)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="4" fill="white"/>
              <line x1="12" y1="2" x2="12" y2="5" stroke="white" stroke-width="2" stroke-linecap="round"/>
              <line x1="12" y1="19" x2="12" y2="22" stroke="white" stroke-width="2" stroke-linecap="round"/>
              <line x1="2" y1="12" x2="5" y2="12" stroke="white" stroke-width="2" stroke-linecap="round"/>
              <line x1="19" y1="12" x2="22" y2="12" stroke="white" stroke-width="2" stroke-linecap="round"/>
              <line x1="4.93" y1="4.93" x2="7.05" y2="7.05" stroke="white" stroke-width="2" stroke-linecap="round"/>
              <line x1="16.95" y1="16.95" x2="19.07" y2="19.07" stroke="white" stroke-width="2" stroke-linecap="round"/>
              <line x1="19.07" y1="4.93" x2="16.95" y2="7.05" stroke="white" stroke-width="2" stroke-linecap="round"/>
              <line x1="7.05" y1="16.95" x2="4.93" y2="19.07" stroke="white" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <div>
            <div class="text-sm font-bold" style="color:#E8EDF5">Circadian</div>
            <div class="text-xs" style="color:#6B7FA3">Intelligence Platform</div>
          </div>
        </div>
      </div>

      <!-- Nav -->
      <nav class="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <nuxt-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-link flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium cursor-pointer"
          :class="$route.path === item.to || $route.path.startsWith(item.to + '/') ? 'active' : ''"
          style="color: #6B7FA3"
          active-class="active"
          exact-active-class=""
        >
          <span class="w-5 h-5 flex-shrink-0" v-html="item.icon"></span>
          {{ item.label }}
        </nuxt-link>
      </nav>

      <!-- User info -->
      <div class="px-4 py-4 border-t" style="border-color:#1E2F50">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold" style="background:#0860FF30; color:#0860FF">
            DU
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-sm font-medium truncate" style="color:#E8EDF5">Demo User</div>
            <div class="text-xs truncate capitalize" style="color:#6B7FA3">night owl chronotype</div>
          </div>
          <div class="w-2 h-2 rounded-full" style="background:#00C896"></div>
        </div>
      </div>

    </aside>

    <!-- Main content -->
    <div class="flex-1 flex flex-col overflow-hidden">

      <!-- Topbar -->
      <header class="flex-shrink-0 flex items-center justify-between px-8 py-4 border-b" style="background:#0F1F3D; border-color:#1E2F50">
        <div>
          <h1 class="text-lg font-semibold" style="color:#E8EDF5">{{ pageTitle }}</h1>
          <p class="text-xs mt-0.5" style="color:#6B7FA3">{{ pageSubtitle }}</p>
        </div>
        <div class="flex items-center gap-3">

          <div class="text-xs px-3 py-1.5 rounded-full border font-mono" style="background:#162040; border-color:#1E2F50; color:#6B7FA3">
            {{ currentTime }}
          </div>
          <div class="w-2 h-2 rounded-full" style="background:#00C896; box-shadow: 0 0 8px #00C89660"></div>
          <span class="text-xs" style="color:#6B7FA3">Live</span>
        </div>
      </header>

      <!-- Page -->
      <main class="flex-1 overflow-y-auto px-8 py-6">
        <nuxt />
      </main>

    </div>

  </div>
</template>

<script>
export default {
  name: 'DefaultLayout',
  data: function() {
    return {
      currentTime: '',
      timer: null,
      navItems: [
        {
          to: '/circadian',
          label: 'Dashboard',
          icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>'
        },
        {
          to: '/circadian/timeline',
          label: 'Timeline',
          icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'
        },
        {
          to: '/circadian/interventions',
          label: 'Interventions',
          icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
        },
        {
          to: '/circadian/trends',
          label: 'Trends',
          icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
        },

      ]
    }
  },
  computed: {

    pageTitle: function() {
      var path = this.$route.path
      if (path === '/circadian') return 'Circadian Dashboard'
      if (path.includes('timeline')) return 'Circadian Timeline'
      if (path.includes('interventions')) return 'Interventions'
      if (path.includes('trends')) return 'Trends & Forecast'
      return 'Circadian Intelligence'
    },
    pageSubtitle: function() {
      var path = this.$route.path
      if (path === '/circadian') return 'Real-time physiological intelligence overview'
      if (path.includes('timeline')) return 'Your biological day mapped in real time'
      if (path.includes('interventions')) return 'Personalised zeitgeber recommendations'
      if (path.includes('trends')) return 'Longitudinal circadian health analysis'
      return ''
    }
  },
  mounted: function() {
    this.updateTime()
    this.timer = setInterval(this.updateTime, 1000)
  },
  beforeDestroy: function() {
    if (this.timer) clearInterval(this.timer)
  },
  methods: {
    updateTime: function() {
      var now = new Date()
      this.currentTime = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    },

  }
}
</script>
