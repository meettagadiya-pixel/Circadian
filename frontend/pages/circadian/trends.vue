<template>
  <div class="space-y-5">

    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="skeleton h-32"></div>
    </div>

    <div v-else-if="error" class="flex flex-col items-center justify-center py-24 text-center">
      <div class="text-sm mb-4" style="color:#FF4757">{{ error }}</div>
      <button @click="load" class="px-5 py-2.5 rounded-xl text-sm font-semibold" style="background:#FF9A09; color:#0A1628">Retry</button>
    </div>

    <div v-else>

      <!-- Sleep & Alignment deltas detail -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">

        <div class="c-card animate-fade-up stagger-2">
          <div class="text-sm font-semibold mb-5" style="color:#E8EDF5">Sleep Delta (7-day trend)</div>
          <div class="flex items-end gap-4 mb-4">
            <div class="text-4xl font-bold font-mono" :style="{ color: sleepDeltaColor }">
              {{ sleepDelta != null ? (sleepDelta >= 0 ? '+' : '') + sleepDelta.toFixed(2) : '-' }}
              <span class="text-base font-sans font-normal" style="color:#6B7FA3">h</span>
            </div>
            <div class="text-sm pb-2" style="color:#6B7FA3">change in sleep duration</div>
          </div>
          <div class="p-3 rounded-xl text-xs" style="background:#0F1F3D; color:#6B7FA3; line-height:1.6">
            {{ sleepDelta != null && sleepDelta > 0
              ? 'Sleep duration has increased over the past week — a positive recovery signal.'
              : 'Sleep duration has decreased over the past week. Prioritise consistent bedtimes.' }}
          </div>
        </div>

        <div class="c-card animate-fade-up stagger-3">
          <div class="text-sm font-semibold mb-5" style="color:#E8EDF5">Alignment Delta</div>
          <div class="flex items-end gap-4 mb-4">
            <div class="text-4xl font-bold font-mono" :style="{ color: alignDeltaColor }">
              {{ alignDelta != null ? (alignDelta >= 0 ? '+' : '') + alignDelta.toFixed(2) : '-' }}
            </div>
            <div class="text-sm pb-2" style="color:#6B7FA3">circadian alignment shift</div>
          </div>
          <div class="p-3 rounded-xl text-xs" style="background:#0F1F3D; color:#6B7FA3; line-height:1.6">
            {{ alignDelta != null && alignDelta >= 0
              ? 'Circadian alignment is stable or improving.'
              : 'Circadian alignment is deteriorating. Increase morning light and sleep consistency.' }}
          </div>
        </div>

      </div>

      <!-- Trend alerts -->
      <div v-if="trendAlerts.length" class="c-card animate-fade-up stagger-3">
        <div class="text-sm font-semibold mb-4" style="color:#E8EDF5">Trend Alerts</div>
        <div class="space-y-3">
          <div v-for="(alert, i) in trendAlerts" :key="i"
            class="flex items-start gap-4 p-4 rounded-xl"
            :style="alert.severity === 'high'
              ? 'background:#FF475715; border:1px solid #FF475740'
              : 'background:#FF9A0915; border:1px solid #FF9A0940'">
            <div class="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
              :style="{ background: alert.severity === 'high' ? '#FF475725' : '#FF9A0925' }">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
                :stroke="alert.severity === 'high' ? '#FF4757' : '#FF9A09'"
                stroke-width="2" stroke-linecap="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
            </div>
            <div class="flex-1">
              <div class="text-xs font-semibold mb-1 capitalize" :style="{ color: alert.severity === 'high' ? '#FF4757' : '#FF9A09' }">
                {{ (alert.type || 'Alert').replace(/_/g, ' ') }}
                <span class="ml-1.5 text-xs px-1.5 py-0.5 rounded-full" :style="{ background: alert.severity === 'high' ? '#FF475720' : '#FF9A0920' }">{{ alert.severity }}</span>
              </div>
              <p class="text-sm" style="color:#6B7FA3">{{ alert.message }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Readiness Drivers — detailed breakdown, unique to Trends -->
      <div class="c-card animate-fade-up stagger-4">
        <div class="text-sm font-semibold mb-5" style="color:#E8EDF5">Readiness Drivers</div>
        <div class="grid grid-cols-2 lg:grid-cols-5 gap-4">
          <div v-for="(val, key) in readinessDrivers" :key="key" class="text-center p-3 rounded-xl" style="background:#0F1F3D">
            <div class="text-xs mb-2 capitalize" style="color:#6B7FA3">{{ key === 'risk_score' ? 'Stress Index' : key.replace(/_/g,' ') }}</div>
            <div class="text-xl font-bold font-mono" :style="{ color: driverColor(key, val) }">{{ val != null ? val : '-' }}</div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
var API = process.env.CIRCADIAN_API_URL || 'http://localhost:8000'


export default {
  name: 'CircadianTrends',
  data: function() {
    return { loading: true, error: null, data: null }
  },
  computed: {
    userId: function() { return this.$userStore ? this.$userStore.userId : '659f5c51-ca99-4f1b-85b9-9bc0185fff36' },
    summary: function() { return this.data && this.data.summary ? this.data.summary : {} },
    trends: function() { return this.data && this.data.trends ? this.data.trends : {} },
    readiness: function() { return this.data && this.data.readiness ? this.data.readiness : {} },
    sleepDelta: function() { return this.trends.sleep_delta != null ? this.trends.sleep_delta : null },
    alignDelta: function() { return this.trends.alignment_delta != null ? this.trends.alignment_delta : null },
    sleepDeltaColor: function() {
      if (this.sleepDelta == null) return '#6B7FA3'
      return this.sleepDelta >= 0 ? '#00C896' : '#FF4757'
    },
    alignDeltaColor: function() {
      if (this.alignDelta == null) return '#6B7FA3'
      return this.alignDelta >= 0 ? '#00C896' : '#FF4757'
    },
    trendAlerts: function() { return this.trends.trends || [] },
    readinessDrivers: function() { return this.readiness.drivers || {} }
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
    driverColor: function(key, val) {
      if (key === 'avg_hrv') return val > 30 ? '#00C896' : '#FF4757'
      if (key === 'fatigue_prediction') return val > 3 ? '#FF4757' : '#00C896'
      if (key === 'risk_score') return val > 50 ? '#FF4757' : '#00C896'
      if (key === 'alignment_score') return val > 50 ? '#00C896' : '#FF4757'
      if (key === 'adherence_score') return val > 60 ? '#00C896' : '#FF9A09'
      return '#E8EDF5'
    }
  }
}
</script>