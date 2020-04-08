<template>
  <div class="new-game">
    <h1 class="title">New Game</h1>
    <b-field label="#Cards per player">
      <b-input v-model="game.maxCards"/>
    </b-field>
    <h3 class="title is-3">Teams</h3>
    <b-button v-on:click="addTeam" class="add-team">
      Add Team
    </b-button>
    <b-button v-on:click="removeTeam" class="remove-team">
      Remove Team
    </b-button>
    <hr/>
    <div v-for="(team, idx) in game.teams" :key="idx">
      <div class="columns">
        <div class="column">
          <h4 class="title is-4">Name</h4>
          <b-input v-model="team.name" class="team-name" />
          <div class="team-actions">
            <b-button v-on:click="addPlayer(idx)" class="add-player">
              Add player
            </b-button>
            <b-button v-on:click="removePlayer(idx)" class="remove-player">
              Remove player
            </b-button>
          </div>
        </div>
        <div class="column">
          <h4 class="title is-4">Players</h4>
          <div v-for="(player, idx) in team.players" :key="idx">
            <b-input v-model="player.name" class="player-name" />
          </div>
        </div>
      </div>
      <hr/>
    </div>
    <div class="game-actions">
      <b-button v-on:click="createGame" class="is-primary">
        Create Game
      </b-button>
    </div>
    <b-loading
      :is-full-page="true"
      :active.sync="isLoading"
      :can-cancel="false"/>
  </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';
import axios from 'axios';

const createTeam = (name) => ({ name, players: [{ name: 'Player 1' }] });

@Component
export default class NewGame extends Vue {
  games = ['Game 1', 'Game 2'];

  game = { maxCards: 5, teams: [createTeam('Team 1'), createTeam('Team 2')] };

  isLoading = false

  createGame() {
    if (this.isLoading) {
      return;
    }
    this.isLoading = true;
    axios
      .put('http://localhost:5000/games', this.game)
      .then(() => {
        this.$router.replace('/');
      })
      .catch((error) => {
        this.isLoading = false;
        console.log(error);
        this.$buefy.dialog.alert('There was an error');
      });
  }

  addTeam() {
    const { teams } = this.game;
    teams.push(createTeam(`Team ${teams.length + 1}`));
  }

  removeTeam() {
    const { teams } = this.game;
    if (teams) {
      teams.pop();
    }
  }

  addPlayer(teamIdx) {
    const { players } = this.game.teams[teamIdx];
    players.push({ name: `Player ${players.length + 1}` });
  }

  removePlayer(teamIdx) {
    const { players } = this.game.teams[teamIdx];
    if (players) {
      players.pop();
    }
  }
}
</script>

<style scoped lang="scss">
  .team-actions {
    margin-top: 10px;
    display: flex;
    justify-content: flex-end;
  }

  .game-actions {
    display: flex;
    justify-content: flex-end;
  }

  .add-player {
    margin-right: 10px;
  }

  .player-name {
    margin-bottom: 10px;
  }

  .add-team {
    margin-right: 10px;
  }
</style>
