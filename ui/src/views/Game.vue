<template>
  <div class="game" v-if="game">
    <Navbar/>
    <div class="section">
      <div class="container">
        <div v-for="team in game.teams" :key="team.id" class="team">
          <h2 class="title is-2">{{team.name}} ({{team.guessedCount}})</h2>
          <b-table :data="team.players" striped hoverable>
            <template slot-scope="props">
              <b-table-column field="name" label="Name">
                {{props.row.name}}
              </b-table-column>
              <b-table-column field="created_count" label="Created" centered>
                <span class="tag"
                  v-bind:class="{
                    'is-warning': props.row.createdCount < game.maxCards,
                    'is-success': props.row.createdCount == game.maxCards,
                    'is-error': props.row.createdCount > game.maxCards,
                  }"
                >
                  {{props.row.createdCount}}
                </span>
              </b-table-column>
              <b-table-column field="guessed_count" label="Guessed" centered>
                <span class="tag">{{props.row.guessedCount}}</span>
              </b-table-column>
              <b-table-column label="Actions" numeric>
                <div class="buttons">
                  <router-link
                    :to="`/games/${game.id}/add_cards?playerId=${props.row.id}`"
                    class="button">
                    Add Cards
                  </router-link>
                  <router-link
                    :to="`/games/${game.id}/play?playerId=${props.row.id}`"
                    class="button is-success" >
                    Play
                  </router-link>
                </div>
              </b-table-column>
            </template>
          </b-table>
        </div>
        <div class="game-actions">
        <b-button class="is-large" v-on:click="nextRound">Next Round</b-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Component, Vue, Prop } from 'vue-property-decorator';
import axios from 'axios';

import Navbar from '../components/Navbar.vue';

@Component({ components: { Navbar } })
export default class Games extends Vue {
  @Prop(String) gameId

  game = null

  mounted() {
    axios
      .get(`${this.$API}/games/${this.gameId}`)
      .then((response) => {
        this.game = response.data;
      })
      .catch(this.errorAlert);
  }

  nextRound() {
    axios
      .post(`${this.$API}/games/${this.gameId}/next_round`)
      .then((response) => {
        this.game = response.data.game;
      })
      .catch(this.errorAlert);
  }

  errorAlert(error) {
    this.isLoading = false;
    console.log(error);
    this.$buefy.dialog.alert('There was an error');
  }
}
</script>

<style scoped lang="scss">
  .buttons {
    display: inline;
  }

  .team {
    margin-bottom: 30px;
  }

  .game-actions {
    display: flex;
    justify-content: center;
    margin-top: 30px;
  }
</style>
