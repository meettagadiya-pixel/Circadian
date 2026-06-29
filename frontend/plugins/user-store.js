// plugins/user-store.js
// Single user store — switcher removed for production handover.
// To add multi-user support in future, restore the USERS array
// and switchTo() method, and connect real provider accounts.

import Vue from 'vue'

var store = Vue.observable({
  userId: '659f5c51-ca99-4f1b-85b9-9bc0185fff36',
  label: 'Demo User',
  chronotype: 'night_owl'
})

var userStore = {
  get userId()    { return store.userId },
  get label()     { return store.label },
  get chronotype(){ return store.chronotype }
}

export default function(context, inject) {
  inject('userStore', userStore)
}
