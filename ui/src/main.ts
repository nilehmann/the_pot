import Vue from 'vue';
import Buefy from 'buefy';
import 'buefy/dist/buefy.css';
import App from './App.vue';
import router from './router';

Vue.config.productionTip = false;
Vue.use(Buefy);

const plugin = {
  install() {
    Vue.prototype.$API = process.env.VUE_APP_API;
  },
};

Vue.use(plugin);

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
