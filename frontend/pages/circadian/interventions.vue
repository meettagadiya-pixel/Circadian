<template>
  <div class="space-y-5">

    <div v-if="loading" class="space-y-4">
      <div v-for="i in 4" :key="i" class="skeleton h-24"></div>
    </div>

    <div v-else-if="error" class="flex flex-col items-center justify-center py-24 text-center">
      <div class="text-sm mb-4" style="color:#FF4757">{{ error }}</div>
      <button @click="load" class="px-5 py-2.5 rounded-xl text-sm font-semibold" style="background:#FF9A09; color:#0A1628">Retry</button>
    </div>

    <div v-else>

      <!-- Summary strip -->
      <div class="grid grid-cols-3 gap-4">
        <div class="c-card animate-fade-up stagger-1 text-center">
          <div class="text-3xl font-bold font-mono mb-1" :style="{ color: urgentCount > 0 ? '#FF4757' : '#00C896' }">{{ urgentCount }}</div>
          <div class="text-xs" style="color:#6B7FA3">High priority</div>
        </div>
        <div class="c-card animate-fade-up stagger-2 text-center">
          <div class="text-3xl font-bold font-mono mb-1" style="color:#FF9A09">{{ interventions.length }}</div>
          <div class="text-xs" style="color:#6B7FA3">Active zeitgebers</div>
        </div>
        <div class="c-card animate-fade-up stagger-3 text-center">
          <div class="text-3xl font-bold font-mono mb-1" style="color:#0860FF">{{ scheduledTodayCount }}</div>
          <div class="text-xs" style="color:#6B7FA3">Scheduled today</div>
        </div>
      </div>

      <!-- Tab filter -->
      <div class="flex gap-2 flex-wrap">
        <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key"
          class="px-4 py-2 rounded-xl text-sm font-medium transition-all"
          :style="activeTab === tab.key
            ? 'background:#FF9A09; color:#0A1628'
            : 'background:#162040; color:#6B7FA3; border:1px solid #1E2F50'">
          {{ tab.label }}
          <span v-if="tab.count != null" class="ml-1.5 text-xs opacity-75">({{ tab.count }})</span>
        </button>
      </div>

      <!-- ─── ZEITGEBERS TAB ─────────────────────────── -->
      <div v-if="activeTab === 'all' || activeTab === 'zeitgebers'">
        <div class="flex items-center gap-2 mb-3">
          <div class="w-2 h-2 rounded-full animate-pulse" style="background:#FF4757"></div>
          <span class="text-sm font-semibold" style="color:#E8EDF5">Active Zeitgebers</span>
          <span class="text-xs" style="color:#6B7FA3">— personalised time-giver interventions</span>
        </div>
        <div v-if="!interventions.length" class="c-card py-8 text-center">
          <div class="text-sm font-semibold mb-1" style="color:#E8EDF5">All clear</div>
          <div class="text-xs" style="color:#6B7FA3">No active interventions right now</div>
        </div>
        <div class="space-y-3">
          <div v-for="(item, i) in interventions" :key="'z-'+i"
            class="c-card animate-fade-up flex items-start gap-4"
            :style="item.priority === 'high' ? 'border-left: 3px solid #FF4757' :
                    item.priority === 'medium' ? 'border-left: 3px solid #FF9A09' :
                    'border-left: 3px solid #00C896'">
            <div class="w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0" :style="{ background: typeColor(item.type) + '20' }">
              <svg v-if="item.type === 'light_exposure'" width="18" height="18" viewBox="0 0 24 24" fill="none" :stroke="typeColor(item.type)" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/></svg>
              <svg v-else-if="item.type === 'sleep_timing' || item.type === 'sleep_schedule'" width="18" height="18" viewBox="0 0 24 24" fill="none" :stroke="typeColor(item.type)" stroke-width="2" stroke-linecap="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
              <svg v-else-if="item.type === 'nutrition'" width="18" height="18" viewBox="0 0 24 24" fill="none" :stroke="typeColor(item.type)" stroke-width="2" stroke-linecap="round"><path d="M18 8h1a4 4 0 0 1 0 8h-1"/><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>
              <svg v-else-if="item.type === 'exercise_timing'" width="18" height="18" viewBox="0 0 24 24" fill="none" :stroke="typeColor(item.type)" stroke-width="2" stroke-linecap="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              <svg v-else-if="item.type === 'recovery'" width="18" height="18" viewBox="0 0 24 24" fill="none" :stroke="typeColor(item.type)" stroke-width="2" stroke-linecap="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
              <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" :stroke="typeColor(item.type)" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1.5">
                <span class="text-sm font-semibold capitalize" style="color:#E8EDF5">{{ formatType(item.type) }}</span>
                <span v-if="item.priority === 'high'" class="text-xs px-2 py-0.5 rounded-full font-medium" style="background:#FF475720; color:#FF4757">High priority</span>
                <span v-else-if="item.priority === 'medium'" class="text-xs px-2 py-0.5 rounded-full font-medium" style="background:#FF9A0920; color:#FF9A09">Medium</span>
                <span v-else class="text-xs px-2 py-0.5 rounded-full font-medium" style="background:#00C89620; color:#00C896">Maintenance</span>
              </div>
              <p class="text-sm leading-relaxed" style="color:#6B7FA3">{{ item.message }}</p>
              <div v-if="item.scheduled_time" class="flex items-center gap-1.5 mt-2">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#6B7FA3" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                <span class="text-xs font-mono" style="color:#6B7FA3">Scheduled {{ formatTime(item.scheduled_time) }}</span>
              </div>
            </div>
            <div class="flex-shrink-0">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center" :style="{ background: typeColor(item.type) + '15' }">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" :stroke="typeColor(item.type)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ─── LOG ACTIVITY TAB ───────────────────────── -->
      <div v-if="activeTab === 'all' || activeTab === 'log'">

        <!-- Context explanation -->
        <div class="c-card mb-3 animate-fade-up" style="background:#0F1F3D; border:1px solid #1E2F50">
          <div class="flex items-start gap-3">
            <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0" style="background:#0860FF20">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0860FF" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            </div>
            <div>
              <div class="text-xs font-semibold mb-1" style="color:#E8EDF5">Why log your activity?</div>
              <div class="text-xs leading-relaxed" style="color:#6B7FA3">
                Meal and exercise timing relative to your biological clock (midnight: <span style="color:#FF9A09">{{ bioMidnightStr }}</span>) directly impacts circadian alignment. Logging helps the system generate personalised zeitgeber recommendations instead of generic ones.
              </div>
            </div>
          </div>
        </div>

        <!-- Quick log — confirm before posting -->
        <div class="c-card mb-3">
          <div class="text-xs font-medium mb-1" style="color:#6B7FA3">Quick log</div>
          <div class="text-xs mb-3" style="color:#4A5568">Tap once to select, tap again to confirm</div>
          <div class="grid grid-cols-2 gap-2">
            <button v-for="quick in quickLogs" :key="quick.key"
              @click="selectQuick(quick)"
              class="flex items-center gap-2.5 p-3 rounded-xl text-left transition-all"
              :style="pendingQuick && pendingQuick.key === quick.key
                ? 'background:' + quick.color + '40; border: 2px solid ' + quick.color
                : 'background:' + quick.color + '12; border: 1px solid ' + quick.color + '25'"
              :disabled="logLoading">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
                :style="{ background: quick.color + '25' }">
                <span style="font-size:16px">{{ quick.emoji }}</span>
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-xs font-semibold" :style="{ color: quick.color }">{{ quick.label }}</div>
                <div v-if="pendingQuick && pendingQuick.key === quick.key" class="text-xs font-medium" style="color:#E8EDF5">Tap again to confirm ✓</div>
                <div v-else class="text-xs" style="color:#6B7FA3; font-size:10px">{{ quick.sublabel }}</div>
              </div>
            </button>
          </div>

          <!-- Loading state -->
          <div v-if="logLoading" class="mt-3 flex items-center gap-2 p-3 rounded-xl" style="background:#162040">
            <div class="w-4 h-4 rounded-full border-2 border-t-transparent animate-spin" style="border-color:#FF9A09; border-top-color:transparent"></div>
            <span class="text-xs" style="color:#6B7FA3">Saving...</span>
          </div>
        </div>

        <!-- Custom log form -->
        <div class="c-card">
          <div class="text-xs font-medium mb-3" style="color:#6B7FA3">Custom log — with optional time</div>
          <div class="space-y-3">

            <!-- Event type selector -->
            <div>
              <div class="text-xs mb-2" style="color:#4A5568">What are you logging?</div>
              <div class="grid grid-cols-3 gap-2">
                <button v-for="et in eventTypes" :key="et.value"
                  @click="logForm.event_type = et.value"
                  class="py-2.5 px-3 rounded-xl text-xs font-medium transition-all flex items-center justify-center gap-1.5"
                  :style="logForm.event_type === et.value
                    ? 'background:' + et.color + '; color:#0A1628'
                    : 'background:#162040; color:#6B7FA3; border:1px solid #1E2F50'">
                  <span>{{ et.emoji }}</span>
                  <span>{{ et.label }}</span>
                </button>
              </div>
            </div>

            <!-- Notes input -->
            <div>
              <div class="text-xs mb-2" style="color:#4A5568">Notes</div>
              <input
                v-model="logForm.notes"
                type="text"
                :placeholder="notesPlaceholder"
                class="w-full px-4 py-2.5 rounded-xl text-sm outline-none"
                style="background:#0F1F3D; border:1px solid #1E2F50; color:#E8EDF5"
                maxlength="120"
              />
            </div>

            <!-- Time selector -->
            <div>
              <div class="text-xs mb-2" style="color:#4A5568">When did this happen?</div>
              <div class="flex items-center gap-3 flex-wrap">
                <label class="flex items-center gap-1.5 cursor-pointer">
                  <input type="radio" v-model="logForm.useNow" :value="true"/>
                  <span class="text-xs" style="color:#E8EDF5">Just now <span style="color:#6B7FA3">({{ currentTimeStr }})</span></span>
                </label>
                <label class="flex items-center gap-1.5 cursor-pointer">
                  <input type="radio" v-model="logForm.useNow" :value="false"/>
                  <span class="text-xs" style="color:#E8EDF5">Earlier today</span>
                </label>
                <input v-if="!logForm.useNow"
                  v-model="logForm.customTime"
                  type="time"
                  class="px-3 py-1.5 rounded-lg text-xs outline-none"
                  style="background:#0F1F3D; border:1px solid #1E2F50; color:#E8EDF5"/>
              </div>
            </div>

            <!-- Submit -->
            <button
              @click="submitLog"
              :disabled="!logForm.event_type || !logForm.notes.trim() || logLoading"
              class="w-full py-3 rounded-xl text-sm font-semibold transition-all flex items-center justify-center gap-2"
              :style="logForm.event_type && logForm.notes.trim() && !logLoading
                ? 'background:#00C896; color:#0A1628'
                : 'background:#1E2F50; color:#4A5568; cursor:not-allowed'">
              <svg v-if="!logLoading" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
              <div v-else class="w-4 h-4 rounded-full border-2 border-t-transparent animate-spin" style="border-color:currentColor; border-top-color:transparent"></div>
              {{ logLoading ? 'Saving...' : 'Log Activity' }}
            </button>
          </div>
        </div>

        <!-- Success toast -->
        <div v-if="logSuccess" class="flex items-center gap-3 p-4 rounded-xl animate-fade-up" style="background:#00C89615; border:1px solid #00C89640">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#00C896" stroke-width="2" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
          <div>
            <div class="text-sm font-semibold" style="color:#00C896">{{ logSuccess.title }}</div>
            <div class="text-xs" style="color:#6B7FA3">{{ logSuccess.sub }}</div>
          </div>
        </div>

        <!-- Error toast -->
        <div v-if="logError" class="flex items-center gap-3 p-4 rounded-xl" style="background:#FF475715; border:1px solid #FF475730">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#FF4757" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/></svg>
          <span class="text-sm" style="color:#FF4757">{{ logError }}</span>
        </div>

        <!-- Recent logs -->
        <div v-if="recentLogs.length" class="c-card mt-3">
          <div class="text-xs font-medium mb-3" style="color:#6B7FA3">Recent activity — last 10 logs</div>
          <div class="space-y-2">
            <div v-for="(log, i) in recentLogs" :key="i"
              class="flex items-center gap-3 py-2 border-b last:border-0"
              style="border-color:#1E2F50">
              <div class="w-6 h-6 rounded-lg flex items-center justify-center flex-shrink-0"
                :style="{ background: logTypeColor(log.event_type) + '20' }">
                <span style="font-size:12px">{{ logTypeEmoji(log.event_type) }}</span>
              </div>
              <div class="flex-1 min-w-0">
                <span class="text-xs font-medium capitalize" :style="{ color: logTypeColor(log.event_type) }">{{ log.event_type }}</span>
                <span class="text-xs ml-2" style="color:#6B7FA3">{{ log.notes }}</span>
              </div>
              <span class="text-xs font-mono flex-shrink-0" style="color:#4A5568">{{ formatTime(log.timestamp) }}</span>
            </div>
          </div>
        </div>

      </div>

      <!-- ─── ENVIRONMENT TAB ────────────────────────── -->
      <div v-if="activeTab === 'all' || activeTab === 'environment'">
        <div v-if="lightRecs.length" class="mt-2">
          <div class="flex items-center gap-2 mb-3">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#FF9A09" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/></svg>
            <span class="text-sm font-semibold" style="color:#E8EDF5">Light Exposure Guidance</span>
          </div>
          <div class="space-y-2">
            <div v-for="(rec, i) in lightRecs" :key="i" class="flex items-start gap-3 p-3 rounded-xl" style="background:#0F1F3D; border:1px solid #1E2F50">
              <div class="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0" style="background:#FF9A09"></div>
              <p class="text-sm" style="color:#6B7FA3">{{ rec }}</p>
            </div>
          </div>
        </div>
        <div v-if="daylight" class="c-card mt-3">
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
  </div>
</template>

<script>
var API = process.env.CIRCADIAN_API_URL || 'http://localhost:8000'

function isTodayDate(d) {
  if (!d) return false
  try {
    var dt = new Date(d), now = new Date()
    return dt.getFullYear() === now.getFullYear() && dt.getMonth() === now.getMonth() && dt.getDate() === now.getDate()
  } catch(e) { return false }
}

function fmtTime(d) {
  if (!d) return '-'
  try { return new Date(d).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }
  catch(e) { return String(d) }
}

export default {
  name: 'CircadianInterventions',
  data: function() {
    return {
      loading: true, error: null, data: null,
      activeTab: 'all',
      logLoading: false,
      logSuccess: null,
      logError: null,
      pendingQuick: null,   // first-tap selection
      recentLogs: [],
      currentTimeStr: fmtTime(new Date()),
      timeTimer: null,
      logForm: { event_type: '', notes: '', useNow: true, customTime: '' },
      eventTypes: [
        { value: 'meal',        label: 'Meal',     emoji: '🍽️', color: '#00C896' },
        { value: 'exercise',    label: 'Exercise', emoji: '🏃', color: '#FF9A09' },
        { value: 'sleep_onset', label: 'Sleep',    emoji: '😴', color: '#0860FF' }
      ],
      quickLogs: [
        { key: 'breakfast',        type: 'meal',        notes: 'Breakfast',        label: 'Breakfast',        sublabel: 'Morning meal',         emoji: '🌅', color: '#00C896' },
        { key: 'lunch',            type: 'meal',        notes: 'Lunch',            label: 'Lunch',            sublabel: 'Midday meal',           emoji: '☀️', color: '#00C896' },
        { key: 'dinner',           type: 'meal',        notes: 'Dinner',           label: 'Dinner',           sublabel: 'Evening meal',          emoji: '🌙', color: '#00C896' },
        { key: 'late_snack',       type: 'meal',        notes: 'Late snack',       label: 'Late snack',       sublabel: 'After 9 PM',           emoji: '🍫', color: '#FF4757' },
        { key: 'morning_workout',  type: 'exercise',    notes: 'Morning workout',  label: 'Morning workout',  sublabel: 'Before noon',           emoji: '🏋️', color: '#FF9A09' },
        { key: 'evening_workout',  type: 'exercise',    notes: 'Evening workout',  label: 'Evening workout',  sublabel: 'After 6 PM',            emoji: '🏃', color: '#FF9A09' },
        { key: 'sleep',            type: 'sleep_onset', notes: 'Going to sleep',   label: 'Sleep now',        sublabel: 'Record bedtime',        emoji: '😴', color: '#0860FF' }
      ]
    }
  },
  computed: {
    userId: function() { return this.$userStore ? this.$userStore.userId : '659f5c51-ca99-4f1b-85b9-9bc0185fff36' },
    interventions: function() {
      if (!this.data) return []
      var notifs = this.data.notifications || []
      return notifs.length > 0 ? notifs : (this.data.top_interventions || [])
    },
    urgentCount: function() {
      return this.interventions.filter(function(n) { return n.priority === 'high' || n.urgency === 'high' }).length
    },
    scheduledTodayCount: function() {
      return this.interventions.filter(function(n) { return isTodayDate(n.scheduled_time) }).length
    },
    lightRecs: function() {
      return this.data && this.data.light_exposure_summary && this.data.light_exposure_summary.recommendations
        ? this.data.light_exposure_summary.recommendations : []
    },
    daylight: function() { return this.data && this.data.daylight_context ? this.data.daylight_context : null },
    bioMidnightStr: function() {
      var s = this.data && this.data.summary
      return s && s.biological_midnight ? fmtTime(s.biological_midnight) : '--:--'
    },
    notesPlaceholder: function() {
      if (this.logForm.event_type === 'meal') return "e.g. 'Late dinner with carbs', 'Light salad', 'Pizza'"
      if (this.logForm.event_type === 'exercise') return "e.g. 'HIIT 30 min', 'Morning run', 'Weights session'"
      if (this.logForm.event_type === 'sleep_onset') return "e.g. 'Early night', 'Couldn\\'t sleep until late'"
      return "Describe your activity..."
    },
    tabs: function() {
      return [
        { key: 'all',           label: 'All' },
        { key: 'zeitgebers',    label: 'Zeitgebers',   count: this.interventions.length },
        { key: 'log',           label: 'Log Activity', count: null },
        { key: 'environment',   label: 'Environment',  count: null }
      ]
    }
  },
  mounted: function() {
    this.load()
    this.loadRecentLogs()
    this.$nuxt.$on('user-switched', this.load)
    this.timeTimer = setInterval(function() { this.currentTimeStr = fmtTime(new Date()) }.bind(this), 30000)
  },
  beforeDestroy: function() {
    this.$nuxt.$off('user-switched', this.load)
    if (this.timeTimer) clearInterval(this.timeTimer)
  },
  methods: {
    load: function() {
      var self = this
      self.loading = true; self.error = null
      fetch(API + '/dashboard-summary?user_id=' + self.userId)
        .then(function(r) { if (!r.ok) throw new Error('API error ' + r.status); return r.json() })
        .then(function(d) { self.data = d })
        .catch(function(e) { self.error = e.message })
        .finally(function() { self.loading = false })
    },
    loadRecentLogs: function() {
      var self = this
      fetch(API + '/behavior-logs?user_id=' + self.userId + '&limit=10')
        .then(function(r) { if (!r.ok) return { logs: [] }; return r.json() })
        .then(function(d) { self.recentLogs = d.logs || [] })
        .catch(function() {})
    },
    selectQuick: function(quick) {
      // Two-tap confirmation: first tap selects, second tap confirms
      if (this.logLoading) return
      if (this.pendingQuick && this.pendingQuick.key === quick.key) {
        // Second tap = confirm and log
        this.doLog(quick.type, quick.notes)
        this.pendingQuick = null
      } else {
        // First tap = select (highlight)
        this.pendingQuick = quick
        this.logSuccess = null
        this.logError = null
        // Auto-cancel pending after 4 seconds if not confirmed
        var self = this
        setTimeout(function() {
          if (self.pendingQuick && self.pendingQuick.key === quick.key) {
            self.pendingQuick = null
          }
        }, 4000)
      }
    },
    doLog: function(eventType, notes, customTs) {
      var self = this
      self.logLoading = true; self.logSuccess = null; self.logError = null
      var body = { user_id: self.userId, event_type: eventType, notes: notes }
      if (customTs) body.timestamp = customTs
      fetch(API + '/log-behavior', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
        .then(function(r) { if (!r.ok) throw new Error('API error ' + r.status); return r.json() })
        .then(function() {
          self.logSuccess = {
            title: notes + ' logged ✓',
            sub: 'Saved at ' + fmtTime(new Date()) + ' — interventions will update in ~1 min'
          }
          self.loadRecentLogs()
          setTimeout(function() { self.logSuccess = null }, 5000)
        })
        .catch(function(e) { self.logError = 'Could not save: ' + e.message })
        .finally(function() { self.logLoading = false })
    },
    submitLog: function() {
      if (!this.logForm.event_type || !this.logForm.notes.trim() || this.logLoading) return
      var ts = null
      if (!this.logForm.useNow && this.logForm.customTime) {
        var d = new Date(); var parts = this.logForm.customTime.split(':')
        d.setHours(parseInt(parts[0]), parseInt(parts[1]), 0, 0)
        ts = d.toISOString()
      }
      var self = this
      this.doLog(this.logForm.event_type, this.logForm.notes.trim(), ts)
      this.logForm.notes = ''; this.logForm.event_type = ''
    },
    typeColor: function(t) {
      if (t === 'light_exposure') return '#FF9A09'
      if (t === 'sleep_timing' || t === 'sleep_schedule') return '#0860FF'
      if (t === 'nutrition') return '#00C896'
      if (t === 'exercise_timing') return '#00C896'
      if (t === 'recovery') return '#FF4757'
      return '#6B7FA3'
    },
    logTypeColor: function(t) {
      if (t === 'meal') return '#00C896'
      if (t === 'exercise') return '#FF9A09'
      if (t === 'sleep_onset') return '#0860FF'
      return '#6B7FA3'
    },
    logTypeEmoji: function(t) {
      if (t === 'meal') return '🍽️'
      if (t === 'exercise') return '🏃'
      if (t === 'sleep_onset') return '😴'
      return '📝'
    },
    formatType: function(t) {
      if (!t) return 'Intervention'
      return t.replace(/_/g, ' ').replace(/\b\w/g, function(c) { return c.toUpperCase() })
    },
    formatTime: fmtTime
  }
}
</script>