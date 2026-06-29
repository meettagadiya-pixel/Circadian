<template>
  <div>

    <div v-if="loading" class="space-y-6">
      <div class="grid grid-cols-4 gap-4">
        <div v-for="i in 4" :key="i" class="skeleton h-28 animate-fade-up" :class="'stagger-' + i"></div>
      </div>
      <div class="grid grid-cols-3 gap-4">
        <div class="skeleton h-48 col-span-2"></div>
        <div class="skeleton h-48"></div>
      </div>
    </div>

    <div v-else-if="error" class="flex flex-col items-center justify-center py-24 text-center">
      <div class="w-16 h-16 rounded-2xl flex items-center justify-center mb-4" style="background:#FF475720">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#FF4757" stroke-width="2" stroke-linecap="round">
          <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
      </div>
      <div class="text-base font-semibold mb-2" style="color:#E8EDF5">Could not load data</div>
      <div class="text-sm mb-6" style="color:#6B7FA3">{{ error }}</div>
      <button @click="load" class="px-5 py-2.5 rounded-xl text-sm font-semibold transition-opacity hover:opacity-80" style="background:#FF9A09; color:#0A1628">Retry</button>
    </div>

    <div v-else-if="data" class="space-y-5">

      <div v-if="summary.risk_state === 'high' || summary.risk_state === 'critical'" class="animate-fade-up stagger-1 rounded-2xl px-5 py-4 flex items-center gap-4" style="background: linear-gradient(90deg, #FF475715, #FF475705); border: 1px solid #FF475740">
        <div class="w-3 h-3 rounded-full flex-shrink-0" style="background:#FF4757"></div>
        <div class="flex-1">
          <span class="text-sm font-semibold" style="color:#FF4757">High Circadian Stress Detected</span>
          <span class="text-sm ml-2" style="color:#6B7FA3">Circadian stress index is elevated. Prioritise sleep timing and light exposure today.</span>
        </div>
        <div class="text-xs font-mono px-2 py-1 rounded-lg" style="background:#FF475725; color:#FF4757">CSI {{ summary.risk_score }}</div>
      </div>

      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="c-card animate-fade-up stagger-1 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-20 h-20 rounded-full opacity-10" style="background:#FF9A09; transform: translate(30%, -30%)"></div>
          <div class="text-xs font-medium uppercase tracking-widest mb-3" style="color:#6B7FA3">Chronotype</div>
          <div class="text-xl font-bold capitalize mb-1" style="color:#E8EDF5">{{ formatChronotype(summary.chronotype) }}</div>
          <div class="text-xs mb-3" style="color:#6B7FA3">Bio midnight {{ formatShortTime(summary.biological_midnight) }}</div>
          <div class="inline-flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full" style="background:#FF9A0920; color:#FF9A09">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/></svg>
            {{ formatChronotype(summary.chronotype) }}
          </div>
        </div>

        <div class="c-card animate-fade-up stagger-2 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-20 h-20 rounded-full opacity-10" :style="{ background: misalignmentColor, transform: 'translate(30%, -30%)' }"></div>
          <div class="text-xs font-medium uppercase tracking-widest mb-3" style="color:#6B7FA3">Misalignment</div>
          <div class="text-3xl font-bold font-mono mb-1" :style="{ color: misalignmentColor }">
            {{ summary.misalignment_score != null ? summary.misalignment_score.toFixed(2) : '-' }}
            <span class="text-base font-sans font-normal" style="color:#6B7FA3">h</span>
          </div>
          <div class="text-xs mb-3" style="color:#6B7FA3">Social vs biological clock gap</div>
          <div class="inline-flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full" :style="{ background: misalignmentColor + '20', color: misalignmentColor }">
            {{ misalignmentLabel }}
          </div>
          <div v-if="summary.misalignment_interpretation" class="mt-2 text-xs leading-relaxed" style="color:#6B7FA3">{{ summary.misalignment_interpretation }}</div>
        </div>

        <div class="c-card animate-fade-up stagger-3 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-20 h-20 rounded-full opacity-10" :style="{ background: readinessColor, transform: 'translate(30%, -30%)' }"></div>
          <div class="text-xs font-medium uppercase tracking-widest mb-3" style="color:#6B7FA3">Readiness</div>
          <div class="text-3xl font-bold font-mono mb-1" :style="{ color: readinessColor }">
            {{ readiness.readiness_score != null ? readiness.readiness_score : '-' }}
            <span class="text-base font-sans font-normal" style="color:#6B7FA3">/100</span>
          </div>
          <div class="text-xs capitalize mb-3" style="color:#6B7FA3">{{ readiness.readiness_label || 'No data' }}</div>
          <div class="progress-bar"><div class="progress-fill" :style="{ width: (readiness.readiness_score || 0) + '%', background: readinessColor }"></div></div>
        </div>

        <div class="c-card animate-fade-up stagger-4 relative overflow-hidden">
          <div class="absolute top-0 right-0 w-20 h-20 rounded-full opacity-10" style="background:#0860FF; transform: translate(30%, -30%)"></div>
          <div class="text-xs font-medium uppercase tracking-widest mb-3" style="color:#6B7FA3">Avg HRV</div>
          <div class="text-3xl font-bold font-mono mb-1" style="color:#0860FF">
            {{ summary.avg_hrv != null ? summary.avg_hrv.toFixed(0) : '-' }}
            <span class="text-base font-sans font-normal" style="color:#6B7FA3">ms</span>
          </div>
          <div class="text-xs mb-3" style="color:#6B7FA3">Heart rate variability</div>
          <div class="inline-flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full" style="background:#0860FF20; color:#0860FF">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            Autonomic signal
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div class="lg:col-span-2 c-card animate-fade-up stagger-2">
          <div class="flex items-center justify-between mb-4">
            <div>
              <div class="text-sm font-semibold" style="color:#E8EDF5">Active Zeitgebers</div>
              <div class="text-xs mt-0.5" style="color:#6B7FA3">{{ topInterventions.length }} personalised interventions due now</div>
            </div>
            <nuxt-link to="/circadian/interventions" class="text-xs px-3 py-1.5 rounded-lg transition-opacity hover:opacity-80" style="background:#1E2F50; color:#6B7FA3">View all</nuxt-link>
          </div>
          <div v-if="!topInterventions.length" class="py-6 text-center text-sm" style="color:#6B7FA3">No active interventions</div>
          <div class="flex flex-wrap gap-2 mb-5">
            <div v-for="(item, i) in topInterventions" :key="i"
              class="flex items-center gap-2 px-3 py-2 rounded-xl"
              :style="{ background: interventionColor(item) + '15', border: '1px solid ' + interventionColor(item) + '30' }">
              <div class="w-5 h-5 rounded-md flex items-center justify-center" :style="{ background: interventionColor(item) + '25' }">
                <svg v-if="item.type === 'light_exposure'" width="11" height="11" viewBox="0 0 24 24" fill="none" :stroke="interventionColor(item)" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/></svg>
                <svg v-else-if="item.type === 'sleep_timing'" width="11" height="11" viewBox="0 0 24 24" fill="none" :stroke="interventionColor(item)" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
                <svg v-else width="11" height="11" viewBox="0 0 24 24" fill="none" :stroke="interventionColor(item)" stroke-width="2" stroke-linecap="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
              </div>
              <span class="text-xs font-medium capitalize" :style="{ color: interventionColor(item) }">{{ formatInterventionType(item.type) }}</span>
              <span v-if="item.priority === 'high'" class="text-xs px-1.5 py-0.5 rounded-full font-medium" style="background:#FF475720; color:#FF4757">high</span>
            </div>
          </div>
          <div v-if="topInterventions[0]" class="flex items-start gap-3 p-3 rounded-xl" style="background:#0F1F3D; border:1px solid #1E2F50">
            <div class="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0" :style="{ background: interventionColor(topInterventions[0]) }"></div>
            <p class="text-xs leading-relaxed" style="color:#6B7FA3"><span class="font-medium" style="color:#E8EDF5">Priority: </span>{{ topInterventions[0].message }}</p>
          </div>
          <div class="mt-4 pt-4" style="border-top:1px solid #1E2F50">
            <div class="text-xs font-medium mb-3" style="color:#6B7FA3">Today's adherence</div>
            <div class="grid grid-cols-2 gap-x-6 gap-y-2.5">
              <div v-for="bar in adherenceBars" :key="bar.label">
                <div class="flex items-center justify-between mb-1">
                  <span class="text-xs" style="color:#6B7FA3">{{ bar.label }}</span>
                  <span class="text-xs font-mono font-semibold" :style="{ color: bar.color }">{{ bar.pct }}%</span>
                </div>
                <div class="progress-bar"><div class="progress-fill" :style="{ width: bar.pct + '%', background: bar.color }"></div></div>
              </div>
            </div>
          </div>
        </div>

        <div class="c-card animate-fade-up stagger-3">
          <div class="text-sm font-semibold mb-5" style="color:#E8EDF5">Biomarkers</div>
          <div class="space-y-4">
            <div v-for="bm in biomarkers" :key="bm.label" class="flex items-center justify-between">
              <div class="flex items-center gap-2.5">
                <div class="w-7 h-7 rounded-lg flex items-center justify-center" :style="{ background: bm.color + '20' }">
                  <div class="w-2 h-2 rounded-full" :style="{ background: bm.color }"></div>
                </div>
                <span class="text-xs" style="color:#6B7FA3">{{ bm.label }}</span>
              </div>
              <span class="text-sm font-semibold font-mono" style="color:#E8EDF5">
                {{ bm.value != null ? bm.value : '-' }}<span v-if="bm.unit" class="text-xs font-sans font-normal" style="color:#6B7FA3"> {{ bm.unit }}</span>
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div class="c-card animate-fade-up stagger-2">
          <div class="flex items-center justify-between mb-5">
            <div class="text-sm font-semibold" style="color:#E8EDF5">Glucose (CGM)</div>
            <span class="text-xs px-2 py-1 rounded-lg font-mono" style="background:#1E2F50; color:#6B7FA3">mg/dL</span>
          </div>
          <div class="grid grid-cols-3 gap-3 mb-4">
            <div class="text-center p-2 rounded-xl" style="background:#0F1F3D">
              <div class="text-xs mb-1" style="color:#6B7FA3">Avg</div>
              <div class="text-lg font-bold font-mono" style="color:#E8EDF5">{{ cgm.avg_glucose != null ? cgm.avg_glucose.toFixed(0) : '-' }}</div>
            </div>
            <div class="text-center p-2 rounded-xl" style="background:#0F1F3D">
              <div class="text-xs mb-1" style="color:#6B7FA3">Min</div>
              <div class="text-lg font-bold font-mono" style="color:#00C896">{{ cgm.min_glucose != null ? cgm.min_glucose.toFixed(0) : '-' }}</div>
            </div>
            <div class="text-center p-2 rounded-xl" style="background:#0F1F3D">
              <div class="text-xs mb-1" style="color:#6B7FA3">Max</div>
              <div class="text-lg font-bold font-mono" style="color:#FF4757">{{ cgm.max_glucose != null ? cgm.max_glucose.toFixed(0) : '-' }}</div>
            </div>
          </div>
          <div v-if="glucosePoints.length >= 2">
            <div class="text-xs mb-2" style="color:#6B7FA3">Latest readings</div>
            <svg width="100%" :height="60" viewBox="0 0 300 60" preserveAspectRatio="none">
              <defs>
                <linearGradient id="glucGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#00C896" stop-opacity="0.3"/>
                  <stop offset="100%" stop-color="#00C896" stop-opacity="0"/>
                </linearGradient>
              </defs>
              <path :d="glucoseAreaPath" fill="url(#glucGrad)"/>
              <path :d="glucoseLinePath" fill="none" stroke="#00C896" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="text-xs mt-2" style="color:#6B7FA3">{{ cgm.reading_count }} readings from {{ cgm.source }}</div>
          <div v-if="cgm.high_reading_count > 0" class="mt-3 flex items-center gap-2 p-2 rounded-lg" style="background:#FF475715">
            <div class="w-1.5 h-1.5 rounded-full" style="background:#FF4757"></div>
            <span class="text-xs" style="color:#FF4757">{{ cgm.high_reading_count }} readings above 140 mg/dL</span>
          </div>
        </div>

        <div class="c-card animate-fade-up stagger-3">
          <div class="text-sm font-semibold mb-5" style="color:#E8EDF5">Environment</div>
          <div class="space-y-3">
            <div class="flex items-center justify-between py-2 border-b" style="border-color:#1E2F50">
              <span class="text-xs" style="color:#6B7FA3">Light Status</span>
              <span class="text-xs font-medium capitalize" style="color:#E8EDF5">{{ formatStatus(summary.light_exposure_status) }}</span>
            </div>
            <div class="flex items-center justify-between py-2 border-b" style="border-color:#1E2F50">
              <span class="text-xs" style="color:#6B7FA3">Avg Lux</span>
              <span class="text-xs font-mono font-semibold" style="color:#FF9A09">{{ summary.avg_lux != null ? summary.avg_lux.toFixed(0) : '-' }} lx</span>
            </div>
            <div class="flex items-center justify-between py-2 border-b" style="border-color:#1E2F50">
              <span class="text-xs" style="color:#6B7FA3">UV Index</span>
              <span class="text-xs font-mono font-semibold" style="color:#E8EDF5">{{ summary.uvi != null ? summary.uvi.toFixed(1) : '-' }}</span>
            </div>
            <div class="flex items-center justify-between py-2 border-b" style="border-color:#1E2F50">
              <span class="text-xs" style="color:#6B7FA3">Cloud Cover</span>
              <span class="text-xs font-mono font-semibold" style="color:#E8EDF5">{{ summary.clouds != null ? summary.clouds + '%' : '-' }}</span>
            </div>
            <div class="flex items-center justify-between py-2 border-b" style="border-color:#1E2F50">
              <span class="text-xs" style="color:#6B7FA3">Sunrise</span>
              <span class="text-xs font-mono" style="color:#FF9A09">{{ formatShortTime(summary.sunrise) }}</span>
            </div>
            <div class="flex items-center justify-between py-2">
              <span class="text-xs" style="color:#6B7FA3">Sunset</span>
              <span class="text-xs font-mono" style="color:#0860FF">{{ formatShortTime(summary.sunset) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="animate-fade-up stagger-4 flex flex-wrap gap-2">
        <div v-for="(source, key) in dataSources" :key="key"
          class="text-xs px-3 py-1.5 rounded-full flex items-center gap-1.5"
          style="background:#162040; border:1px solid #1E2F50; color:#6B7FA3">
          <div class="w-1.5 h-1.5 rounded-full" style="background:#00C896"></div>
          <span class="capitalize">{{ key }}</span>
          <span style="color:#1E2F50">|</span>
          <span style="color:#E8EDF5">{{ source }}</span>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
var API = process.env.CIRCADIAN_API_URL || 'http://localhost:8000'

export default {
  name: 'CircadianDashboard',
  data: function() { return { loading: true, error: null, data: null } },
  computed: {
    userId: function() { return this.$userStore ? this.$userStore.userId : '659f5c51-ca99-4f1b-85b9-9bc0185fff36' },
    summary: function() { return this.data && this.data.summary ? this.data.summary : {} },
    readiness: function() { return this.data && this.data.readiness ? this.data.readiness : {} },
    topInterventions: function() { return this.data && this.data.top_interventions ? this.data.top_interventions : [] },
    cgm: function() { return this.data && this.data.cgm_summary ? this.data.cgm_summary : {} },
    dataSources: function() { return this.data && this.data.data_sources ? this.data.data_sources : {} },
    misalignmentColor: function() {
      var s = this.summary.misalignment_score
      if (s == null) return '#6B7FA3'
      if (s <= 1) return '#00C896'
      if (s <= 2) return '#FF9A09'
      return '#FF4757'
    },
    misalignmentLabel: function() {
      var s = this.summary.misalignment_score
      if (s == null) return 'No data'
      if (s <= 1) return 'Well aligned'
      if (s <= 2) return 'Moderate'
      return 'High misalignment'
    },
    readinessColor: function() {
      var s = this.readiness.readiness_score
      if (s == null) return '#6B7FA3'
      if (s >= 70) return '#00C896'
      if (s >= 40) return '#FF9A09'
      return '#FF4757'
    },
    biomarkers: function() {
      var s = this.summary
      var self = this
      return [
        { label: 'CBT Nadir', value: self.formatShortTime(s.cbt_nadir_time), unit: '', color: '#0860FF' },
        { label: 'Consistency Score', value: s.consistency_score != null ? (s.consistency_score * 100).toFixed(0) : null, unit: '%', color: '#00C896' },
        { label: 'Bright Light Events', value: s.bright_light_events != null ? String(s.bright_light_events) : null, unit: '', color: '#FF9A09' },
        { label: 'Night Light Events', value: s.night_light_events != null ? String(s.night_light_events) : null, unit: '', color: '#6B7FA3' },
        { label: 'Glucose Variability', value: s.glucose_variability != null ? s.glucose_variability.toFixed(1) : null, unit: '%', color: '#FF9A09' }
      ]
    },
    adherenceBars: function() {
      var s = this.summary
      var toP = function(v) { return v != null ? Math.round(v <= 1 ? v * 100 : v) : 0 }
      var col = function(p) { return p >= 70 ? '#00C896' : p >= 40 ? '#FF9A09' : '#FF4757' }
      return [
        { label: 'Sleep', pct: toP(s.sleep_adherence) },
        { label: 'Meal Timing', pct: toP(s.meal_adherence) },
        { label: 'Exercise', pct: toP(s.exercise_adherence) },
        { label: 'Overall', pct: toP(s.overall_adherence) }
      ].map(function(b) { return Object.assign({}, b, { color: col(b.pct) }) })
    },
    glucosePoints: function() {
      var r = this.cgm.latest_readings
      if (!r || r.length < 2) return []
      return r.map(function(x) { return x.glucose_mg_dl || 0 })
    },
    glucoseLinePath: function() {
      var pts = this.glucosePoints
      if (pts.length < 2) return ''
      var min = Math.min.apply(null, pts), max = Math.max.apply(null, pts), range = max - min || 1
      var w = 300, h = 60, pad = 4
      return pts.map(function(v, i) {
        var x = (i / (pts.length - 1)) * w
        var y = h - pad - ((v - min) / range) * (h - pad * 2)
        return (i === 0 ? 'M' : 'L') + ' ' + x.toFixed(1) + ' ' + y.toFixed(1)
      }).join(' ')
    },
    glucoseAreaPath: function() { return this.glucoseLinePath ? this.glucoseLinePath + ' L 300 60 L 0 60 Z' : '' }
  },
  mounted: function() {
    this.load()
    this.$nuxt.$on('user-switched', this.load)
  },
  beforeDestroy: function() {
    this.$nuxt.$off('user-switched', this.load)
  },
  methods: {
    load: function() {
      var self = this
      self.loading = true
      self.error = null
      fetch(API + '/dashboard-summary?user_id=' + self.userId)
        .then(function(r) { if (!r.ok) throw new Error('API error ' + r.status); return r.json() })
        .then(function(d) { if (d.status === 'no_data') throw new Error('No data for this user'); self.data = d })
        .catch(function(e) { self.error = e.message })
        .finally(function() { self.loading = false })
    },
    formatChronotype: function(c) { return c ? c.replace(/_/g, ' ') : '-' },
    formatShortTime: function(d) {
      if (!d) return '-'
      try { return new Date(d).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) } catch(e) { return String(d) }
    },
    formatInterventionType: function(t) { return t ? t.replace(/_/g, ' ') : 'Intervention' },
    formatStatus: function(s) { return s ? s.replace(/_/g, ' ') : '-' },
    interventionColor: function(item) {
      if (item.type === 'light_exposure') return '#FF9A09'
      if (item.type === 'sleep_timing') return '#0860FF'
      if (item.type === 'nutrition' || item.type === 'meal_timing') return '#00C896'
      if (item.priority === 'high') return '#FF4757'
      return '#00C896'
    }
  }
}
</script>