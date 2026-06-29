<template>
  <div class="space-y-5">

    <div v-if="loading" class="space-y-4">
      <div v-for="i in 4" :key="i" class="skeleton h-20"></div>
    </div>

    <div v-else-if="error" class="flex flex-col items-center justify-center py-24 text-center">
      <div class="text-sm mb-4" style="color:#FF4757">{{ error }}</div>
      <button @click="load" class="px-5 py-2.5 rounded-xl text-sm font-semibold" style="background:#FF9A09; color:#0A1628">Retry</button>
    </div>

    <div v-else>

      <!--
        3 genuinely different counters:
        - Active alerts = total notifications right now
        - High priority = subset that are urgency/priority high
        - Scheduled today = those with a scheduled_time timestamp that falls on today's date
      -->
      <div class="grid grid-cols-3 gap-4">
        <div class="c-card animate-fade-up stagger-1 text-center">
          <div class="text-3xl font-bold font-mono mb-1" style="color:#E8EDF5">{{ allNotifications.length }}</div>
          <div class="text-xs" style="color:#6B7FA3">Active alerts</div>
        </div>
        <div class="c-card animate-fade-up stagger-2 text-center">
          <div class="text-3xl font-bold font-mono mb-1" style="color:#FF4757">{{ highPriorityCount }}</div>
          <div class="text-xs" style="color:#6B7FA3">High priority</div>
        </div>
        <div class="c-card animate-fade-up stagger-3 text-center">
          <div class="text-3xl font-bold font-mono mb-1" style="color:#FF9A09">{{ scheduledTodayCount }}</div>
          <div class="text-xs" style="color:#6B7FA3">Scheduled today</div>
        </div>
      </div>

      <!-- Notification list -->
      <div class="c-card animate-fade-up stagger-2">
        <div class="text-sm font-semibold mb-5" style="color:#E8EDF5">Active Notifications</div>

        <div v-if="!allNotifications.length" class="py-12 text-center">
          <div class="w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-4" style="background:#1E2F50">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#6B7FA3" stroke-width="1.8" stroke-linecap="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
          </div>
          <div class="text-sm font-semibold mb-1" style="color:#E8EDF5">All clear</div>
          <div class="text-xs" style="color:#6B7FA3">No active notifications right now</div>
        </div>

        <div class="space-y-3">
          <div
            v-for="(n, i) in allNotifications"
            :key="i"
            class="flex items-start gap-4 p-4 rounded-2xl transition-all"
            :style="isHighPriority(n)
              ? 'background:#0F1F3D; border:1px solid #FF475740'
              : 'background:#0F1F3D; border:1px solid #1E2F50'"
          >
            <div class="w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0"
              :style="{ background: notifColor(n) + '20' }">
              <svg v-if="isLightType(n)" width="18" height="18" viewBox="0 0 24 24" fill="none" :stroke="notifColor(n)" stroke-width="2" stroke-linecap="round">
                <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
                <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
                <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
              </svg>
              <svg v-else-if="isSleepType(n)" width="18" height="18" viewBox="0 0 24 24" fill="none" :stroke="notifColor(n)" stroke-width="2" stroke-linecap="round">
                <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
              </svg>
              <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" :stroke="notifColor(n)" stroke-width="2" stroke-linecap="round">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/>
              </svg>
            </div>

            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1.5">
                <span class="text-sm font-semibold" style="color:#E8EDF5">{{ n.title || formatType(n.type) }}</span>
                <span v-if="isHighPriority(n)"
                  class="text-xs px-2 py-0.5 rounded-full font-medium"
                  style="background:#FF475720; color:#FF4757">
                  High priority
                </span>
              </div>
              <p class="text-sm leading-relaxed" style="color:#6B7FA3">{{ n.message || n.body || '' }}</p>
              <div v-if="n.scheduled_time" class="flex items-center gap-1.5 mt-2">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#6B7FA3" stroke-width="2" stroke-linecap="round">
                  <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
                </svg>
                <span class="text-xs font-mono" style="color:#6B7FA3">Scheduled {{ formatTime(n.scheduled_time) }}</span>
              </div>
            </div>

            <div class="flex-shrink-0 pt-1">
              <div class="w-2 h-2 rounded-full"
                :style="{ background: isHighPriority(n) ? '#FF4757' : '#FF9A09',
                  boxShadow: isHighPriority(n) ? '0 0 8px #FF475780' : '0 0 8px #FF9A0980' }">
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Light exposure guidance -->
      <div v-if="lightRecs.length" class="c-card animate-fade-up stagger-3">
        <div class="text-sm font-semibold mb-4" style="color:#E8EDF5">Light Exposure Guidance</div>
        <div class="space-y-3">
          <div v-for="(rec, i) in lightRecs" :key="i"
            class="flex items-start gap-3 p-3 rounded-xl"
            style="background:#0F1F3D">
            <div class="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0" style="background:#FF9A09"></div>
            <p class="text-sm" style="color:#6B7FA3">{{ rec }}</p>
          </div>
        </div>
      </div>

      <!-- Daylight context -->
      <div v-if="daylight" class="c-card animate-fade-up stagger-4">
        <div class="text-sm font-semibold mb-4" style="color:#E8EDF5">Daylight Context</div>
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <div class="p-3 rounded-xl text-center" style="background:#0F1F3D">
            <div class="text-xs mb-1" style="color:#6B7FA3">UV Index</div>
            <div class="text-lg font-bold font-mono" style="color:#FF9A09">{{ daylight.uvi != null ? daylight.uvi.toFixed(1) : '-' }}</div>
          </div>
          <div class="p-3 rounded-xl text-center" style="background:#0F1F3D">
            <div class="text-xs mb-1" style="color:#6B7FA3">Clouds</div>
            <div class="text-lg font-bold font-mono" style="color:#E8EDF5">{{ daylight.clouds != null ? daylight.clouds + '%' : '-' }}</div>
          </div>
          <div class="p-3 rounded-xl text-center" style="background:#0F1F3D">
            <div class="text-xs mb-1" style="color:#6B7FA3">Sunrise</div>
            <div class="text-lg font-bold font-mono" style="color:#FF9A09">{{ formatTime(daylight.sunrise) }}</div>
          </div>
          <div class="p-3 rounded-xl text-center" style="background:#0F1F3D">
            <div class="text-xs mb-1" style="color:#6B7FA3">Sunset</div>
            <div class="text-lg font-bold font-mono" style="color:#0860FF">{{ formatTime(daylight.sunset) }}</div>
          </div>
        </div>
        <div v-if="daylight.recommendations && daylight.recommendations.length" class="mt-3 p-3 rounded-xl" style="background:#0F1F3D">
          <p class="text-xs" style="color:#6B7FA3">{{ daylight.recommendations[0] }}</p>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
var API = process.env.CIRCADIAN_API_URL || 'http://localhost:8000'


function isTodayDate(dateStr) {
  if (!dateStr) return false
  try {
    var d = new Date(dateStr)
    var now = new Date()
    return d.getFullYear() === now.getFullYear() &&
           d.getMonth() === now.getMonth() &&
           d.getDate() === now.getDate()
  } catch(e) { return false }
}

export default {
  name: 'CircadianNotifications',
  data: function() {
    return { loading: true, error: null, data: null }
  },
  computed: {
    userId: function() { return this.$userStore ? this.$userStore.userId : '659f5c51-ca99-4f1b-85b9-9bc0185fff36' },
    allNotifications: function() {
      if (!this.data) return []
      var notifs = this.data.notifications || []
      var interventions = this.data.top_interventions || []
      if (notifs.length > 0) return notifs
      // Fallback: convert zeitgebers to notification format
      return interventions.map(function(item) {
        return {
          title: item.type
            ? item.type.replace(/_/g, ' ').replace(/\b\w/g, function(c) { return c.toUpperCase() })
            : 'Alert',
          message: item.message || '',
          priority: item.priority || 'medium',
          urgency: item.urgency || item.priority || 'medium',
          type: item.type || '',
          scheduled_time: item.scheduled_time || null
        }
      })
    },
    highPriorityCount: function() {
      var self = this
      return this.allNotifications.filter(function(n) { return self.isHighPriority(n) }).length
    },
    // Only count notifications that have a scheduled_time falling on today
    scheduledTodayCount: function() {
      return this.allNotifications.filter(function(n) {
        return isTodayDate(n.scheduled_time)
      }).length
    },
    lightRecs: function() {
      return this.data && this.data.light_exposure_summary && this.data.light_exposure_summary.recommendations
        ? this.data.light_exposure_summary.recommendations : []
    },
    daylight: function() {
      return this.data && this.data.daylight_context ? this.data.daylight_context : null
    }
  },
  mounted: function() {
    this.load()
    this.$nuxt.$on('user-switched', this.load) },
  beforeDestroy: function() {
    this.$nuxt.$off('user-switched', this.load)
  },
  methods: {
    load: function() {
      var self = this
      self.loading = true
      self.error = null
      fetch(API + "/dashboard-summary?user_id=" + self.userId)
        .then(function(r) { if (!r.ok) throw new Error('API error ' + r.status); return r.json() })
        .then(function(d) { self.data = d })
        .catch(function(e) { self.error = e.message })
        .finally(function() { self.loading = false })
    },
    isHighPriority: function(n) {
      return n.priority === 'high' || n.urgency === 'high'
    },
    isLightType: function(n) {
      var t = ((n.title || '') + (n.type || '')).toLowerCase()
      return t.indexOf('light') !== -1 || t.indexOf('morning') !== -1
    },
    isSleepType: function(n) {
      var t = ((n.title || '') + (n.type || '')).toLowerCase()
      return t.indexOf('evening') !== -1 || t.indexOf('sleep') !== -1
    },
    notifColor: function(n) {
      if (this.isHighPriority(n)) return '#FF4757'
      var t = ((n.title || '') + (n.type || '')).toLowerCase()
      if (t.indexOf('light') !== -1 || t.indexOf('morning') !== -1) return '#FF9A09'
      if (t.indexOf('evening') !== -1 || t.indexOf('sleep') !== -1) return '#0860FF'
      return '#6B7FA3'
    },
    formatType: function(t) {
      if (!t) return 'Notification'
      return t.replace(/_/g, ' ').replace(/\b\w/g, function(c) { return c.toUpperCase() })
    },
    formatTime: function(d) {
      if (!d) return '-'
      try { return new Date(d).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }
      catch(e) { return String(d) }
    }
  }
}
</script>
