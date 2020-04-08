<template>
  <div class="home">
    <h2>Game list</h2>
    <div v-for="game in games" :key="game">
      {{game}}
    </div>
  </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Home extends Vue {
  games = ['Game 1', 'Game 2']
}
</script>
