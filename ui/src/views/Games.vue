<template>
  <div class="games">
    <h2>Game list</h2>
    <div v-for="game in games" :key="game.id">
      <router-link :to="`/games/${game.id}`">Game {{game.id}}</router-link>
    </div>
  </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import axios from 'axios';

@Component
export default class Games extends Vue {
  games = []

  mounted() {
    axios
      .get(`${this.$API}/games`)
      .then((response) => {
        this.games = response.data.games;
      });
  }
}
</script>
