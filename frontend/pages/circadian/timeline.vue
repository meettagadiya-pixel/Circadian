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

      <!-- 2 unique timeline-specific cards (not on Dashboard) -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">

        <div class="c-card animate-fade-up stagger-1">
          <div class="text-xs uppercase tracking-widest mb-3 font-medium" style="color:#6B7FA3">Biological Midnight</div>
          <div class="text-2xl font-bold font-mono mb-1" style="color:#E8EDF5">{{ fmtTime(summary.biological_midnight) }}</div>
          <div class="text-xs" style="color:#6B7FA3">Internal sleep midpoint</div>
        </div>

        <div class="c-card animate-fade-up stagger-2">
          <div class="text-xs uppercase tracking-widest mb-3 font-medium" style="color:#6B7FA3">CBT Nadir</div>
          <div class="text-2xl font-bold font-mono mb-1" style="color:#0860FF">{{ fmtTime(summary.cbt_nadir_time) }}</div>
          <div class="text-xs" style="color:#6B7FA3">Lowest body temperature</div>
        </div>

        <div class="c-card animate-fade-up stagger-3">
          <div class="text-xs uppercase tracking-widest mb-3 font-medium" style="color:#6B7FA3">Chronotype</div>
          <div class="text-2xl font-bold font-mono mb-1 capitalize" style="color:#FF9A09">{{ (summary.chronotype || '-').replace(/_/g,' ') }}</div>
          <div class="text-xs" style="color:#6B7FA3">Biological clock type</div>
        </div>

        <div class="c-card animate-fade-up stagger-4">
          <div class="text-xs uppercase tracking-widest mb-3 font-medium" style="color:#6B7FA3">DLMO Estimate</div>
          <div class="text-2xl font-bold font-mono mb-1" style="color:#9B59B6">
            {{ summary.dlmo_estimate ? fmtTime(summary.dlmo_estimate) : '-' }}
          </div>
          <div class="flex items-center gap-1.5 mt-1">
            <div class="text-xs" style="color:#6B7FA3">Melatonin onset</div>
            <span class="text-xs px-1.5 py-0.5 rounded-full" style="background:#6B7FA320; color:#6B7FA3; font-size:9px">est.</span>
          </div>
        </div>

      </div>

      <!-- 24h Clock -->
      <div class="c-card animate-fade-up stagger-2">
        <div class="text-sm font-semibold mb-2" style="color:#E8EDF5">24-Hour Biological Clock</div>
        <div class="text-xs mb-5" style="color:#6B7FA3">Your circadian phase mapped against the solar day</div>

        <div class="flex justify-between mb-2 px-0.5">
          <span v-for="h in ['0h','3h','6h','9h','12h','15h','18h','21h','24h']" :key="h"
            class="text-xs font-mono" style="color:#6B7FA3; font-size:10px">{{ h }}</span>
        </div>

        <div class="relative h-12 rounded-2xl overflow-hidden mb-4" style="background: linear-gradient(90deg, #0A1628 0%, #162040 25%, #FF9A09 50%, #162040 75%, #0A1628 100%)">
          <div v-if="sleepWindow.valid"
            class="absolute top-0 bottom-0 flex items-center justify-center"
            :style="{ left: sleepWindow.left + '%', width: sleepWindow.width + '%', background: 'rgba(8,96,255,0.35)', borderLeft: '2px solid #0860FF', borderRight: '2px solid #0860FF' }">
            <span class="text-xs font-semibold" style="color:#E8EDF5; font-size:10px">Sleep</span>
          </div>
          <div v-if="bioMidnightPct != null" class="absolute top-0 bottom-0 w-0.5" :style="{ left: bioMidnightPct + '%', background: 'white', opacity: 0.8 }"></div>
          <div v-if="cbtNadirPct != null" class="absolute top-0 bottom-0 w-0.5" :style="{ left: cbtNadirPct + '%', background: '#0860FF' }"></div>
          <div class="absolute top-0 bottom-0 w-0.5" :style="{ left: currentTimePct + '%', background: '#00C896', boxShadow: '0 0 8px #00C89680' }"></div>
        </div>

        <div class="flex flex-wrap gap-4">
          <div v-for="leg in legend" :key="leg.label" class="flex items-center gap-1.5">
            <div class="w-3 h-2 rounded-sm" :style="{ background: leg.color }"></div>
            <span class="text-xs" style="color:#6B7FA3; font-size:10px">{{ leg.label }}</span>
          </div>
        </div>
      </div>

      <!-- Events + Phase Analysis -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">

        <!-- Circadian events -->
        <div class="c-card animate-fade-up stagger-3">
          <div class="text-sm font-semibold mb-5" style="color:#E8EDF5">Circadian Events</div>
          <div v-if="!circadianEvents.length" class="py-6 text-center text-sm" style="color:#6B7FA3">No events to display</div>
          <div class="relative">
            <div class="absolute left-3.5 top-0 bottom-0 w-px" style="background:#1E2F50"></div>
            <div v-for="(ev, i) in circadianEvents" :key="i" class="relative pl-9 pb-5 last:pb-0">
              <div class="absolute left-2 w-3 h-3 rounded-full border-2 flex-shrink-0"
                :style="{ background: ev.color, borderColor: '#0A1628', top: '2px' }"></div>
              <div class="text-xs font-mono mb-0.5" style="color:#6B7FA3">{{ ev.time }}</div>
              <div class="flex items-center gap-2">
                <div class="text-sm font-semibold" style="color:#E8EDF5">{{ ev.label }}</div>
                <span v-if="ev.estimated" class="text-xs px-1.5 py-0.5 rounded-full" style="background:#6B7FA320; color:#6B7FA3; font-size:9px">est.</span>
              </div>
              <div class="text-xs mt-0.5" style="color:#6B7FA3">{{ ev.desc }}</div>
            </div>
          </div>
        </div>

        <!-- Phase Analysis — light-focused, unique to this page -->
        <div class="c-card animate-fade-up stagger-4">
          <div class="text-sm font-semibold mb-5" style="color:#E8EDF5">Phase Analysis</div>
          <div class="space-y-3">
            <div v-for="row in phaseRows" :key="row.label"
              class="flex items-center justify-between py-2.5 px-3 rounded-xl"
              style="background:#0F1F3D">
              <span class="text-xs" style="color:#6B7FA3">{{ row.label }}</span>
              <span class="text-sm font-semibold font-mono capitalize" :style="{ color: row.color || '#E8EDF5' }">{{ row.value }}</span>
            </div>
          </div>

          <div v-if="trend" class="mt-4 p-3 rounded-xl"
            :style="{ background: trendAlertColor + '15', border: '1px solid ' + trendAlertColor + '40' }">
            <div class="flex items-center gap-1.5 mb-1">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" :stroke="trendAlertColor" stroke-width="2" stroke-linecap="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
              <span class="text-xs font-semibold capitalize" :style="{ color: trendAlertColor }">
                {{ trend.severity === 'low' || trend.type === 'stable' ? 'Stable' : 'Trend Alert' }}
              </span>
              <span class="text-xs px-1.5 py-0.5 rounded-full capitalize"
                :style="{ background: trendAlertColor + '20', color: trendAlertColor }">
                {{ trend.severity || 'low' }}
              </span>
            </div>
            <div class="text-xs" style="color:#6B7FA3">{{ trend.message }}</div>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<script>
var API = process.env.CIRCADIAN_API_URL || 'http://localhost:8000'


function timeToPct(str) {
  if (!str) return null
  try {
    var d = new Date(str)
    var h = d.getUTCHours() + d.getUTCMinutes() / 60
    return Math.round((h / 24) * 100 * 10) / 10
  } catch(e) { return null }
}

function fmtTime(str) {
  if (!str) return '-'
  try { return new Date(str).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }
  catch(e) { return str }
}

export default {
  name: 'CircadianTimeline',
  data: function() {
    return {
      loading: true, error: null, data: null,
      legend: [
        { label: 'Sleep window', color: 'rgba(8,96,255,0.5)' },
        { label: 'Biological midnight', color: 'white' },
        { label: 'CBT Nadir', color: '#0860FF' },
        { label: 'Now', color: '#00C896' }
      ]
    }
  },
  computed: {
    userId: function() { return this.$userStore ? this.$userStore.userId : '659f5c51-ca99-4f1b-85b9-9bc0185fff36' },
    summary: function() { return this.data && this.data.summary ? this.data.summary : {} },
    trends: function() { return this.data && this.data.trends ? this.data.trends : {} },
    misalignmentColor: function() {
      var s = this.summary.misalignment_score
      if (s == null) return '#6B7FA3'
      if (s <= 1) return '#00C896'
      if (s <= 2) return '#FF9A09'
      return '#FF4757'
    },
    bioMidnightPct: function() { return timeToPct(this.summary.biological_midnight) },
    cbtNadirPct: function() { return timeToPct(this.summary.cbt_nadir_time) },
    currentTimePct: function() {
      var now = new Date()
      return Math.round(((now.getHours() + now.getMinutes() / 60) / 24) * 100 * 10) / 10
    },
    sleepWindow: function() {
      var bio = this.bioMidnightPct
      if (bio == null) return { valid: false }
      return { valid: true, left: (bio - 17 + 100) % 100, width: 33 }
    },
    circadianEvents: function() {
      var s = this.summary
      var evs = []
      // DLMO: melatonin onset, shown first as it marks start of biological night
      if (s.dlmo_estimate) evs.push({
        time: fmtTime(s.dlmo_estimate),
        label: 'DLMO (estimated)',
        desc: 'Dim light melatonin onset — biological night begins. Avoid bright light from this point.',
        color: '#9B59B6',
        estimated: true
      })
      if (s.biological_midnight) evs.push({
        time: fmtTime(s.biological_midnight),
        label: 'Biological Midnight',
        desc: 'Peak melatonin, deepest sleep phase',
        color: '#E8EDF5'
      })
      if (s.sunrise) evs.push({
        time: fmtTime(s.sunrise),
        label: 'Sunrise',
        desc: 'Natural zeitgeber — morning light window',
        color: '#FF9A09'
      })
      if (s.cbt_nadir_time) evs.push({
        time: fmtTime(s.cbt_nadir_time),
        label: 'CBT Nadir (estimated)',
        desc: 'Core body temperature minimum — alertness starts rising after this point',
        color: '#0860FF',
        estimated: true
      })
      if (s.sunset) evs.push({
        time: fmtTime(s.sunset),
        label: 'Sunset',
        desc: 'Begin reducing bright light exposure',
        color: '#FF9A0980'
      })
      return evs.sort(function(a, b) { return a.time < b.time ? -1 : 1 })
    },
    // Phase Analysis: light timing quality — unique to this page
    phaseRows: function() {
      var s = this.summary
      return [
        { label: 'Daylight Quality', value: (s.daylight_quality || '-').replace(/_/g,' '), color: '#E8EDF5' },
        { label: 'Light Exposure Status', value: (s.light_exposure_status || '-').replace(/_/g,' '), color: '#E8EDF5' },
        { label: 'Avg Lux', value: s.avg_lux != null ? s.avg_lux.toFixed(0) + ' lx' : '-', color: '#FF9A09' },
        { label: 'Bright Light Events', value: s.bright_light_events != null ? String(s.bright_light_events) : '-', color: s.bright_light_events > 0 ? '#00C896' : '#FF4757' },
        { label: 'Night Light Events', value: s.night_light_events != null ? String(s.night_light_events) : '-', color: s.night_light_events > 0 ? '#FF4757' : '#00C896' },
        { label: 'DLMO Estimate', value: s.dlmo_estimate ? fmtTime(s.dlmo_estimate) : '-', color: '#9B59B6' },
        { label: 'Consistency Score', value: s.consistency_score != null ? (s.consistency_score * 100).toFixed(0) + '%' : '-', color: s.consistency_score != null && s.consistency_score >= 0.6 ? '#00C896' : '#FF9A09' }
      ]
    },
    trend: function() {
      var t = this.trends
      if (!t || !t.trends || !t.trends.length) return null
      return t.trends[0]
    },
    // Colour the trend alert by actual severity, not always red
    trendAlertColor: function() {
      var t = this.trend
      if (!t) return '#6B7FA3'
      var sev = (t.severity || '').toLowerCase()
      var type = (t.type || '').toLowerCase()
      if (sev === 'high') return '#FF4757'
      if (sev === 'medium') return '#FF9A09'
      // stable or low severity = green/teal — it's informational, not alarming
      if (sev === 'low' || type === 'stable' || (t.message || '').toLowerCase().indexOf('stable') !== -1) return '#00C896'
      return '#FF9A09'
    }
  },
  mounted: function() {
    this.load()
    this.$nuxt.$on('user-switched', this.load)
  },
  beforeDestroy: function() {
    this.$nuxt.$off('user-switched', this.load)
  },
  methods: {
    fmtTime: fmtTime,
    load: function() {
      var self = this
      self.loading = true
      self.error = null
      fetch(API + '/dashboard-summary?user_id=' + self.userId)
        .then(function(r) { if (!r.ok) throw new Error('API error ' + r.status); return r.json() })
        .then(function(d) { self.data = d })
        .catch(function(e) { self.error = e.message })
        .finally(function() { self.loading = false })
    }
  }
}
</script>