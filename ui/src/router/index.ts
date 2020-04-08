import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import Home from '../views/Home.vue';
import Games from '../views/Games.vue';
import Game from '../views/Game.vue';
import NewGame from '../views/NewGame.vue';
import AddCards from '../views/AddCards.vue';
import Play from '../views/Play.vue';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/',
    component: Home,
    children: [
      {
        path: '/',
        component: Games,
      },
      {
        path: '/new',
        component: NewGame,
      },
    ],
  },
  {
    path: '/games/:gameId',
    component: Game,
    props: true,
  },
  {
    path: '/games/:gameId/add_cards',
    component: AddCards,
    props: true,
  },
  {
    path: '/games/:gameId/play',
    component: Play,
    props: true,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
