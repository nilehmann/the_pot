<template>
  <div class="home">
    <h2>New Game</h2>
    Number of cards: <input v-model="ncards"/>
    <h3>Teams</h3>
    <hr/>
    <div v-for="(team, idx) in teams" :key="idx">
      Name: <input v-model="team.name" />
      <h4>Players</h4>
      <div v-for="(player, idx) in team.players" :key="idx">
        <input v-model="player.name">
      </div>
      <button v-on:click="addPlayer(idx)">Add player</button>
      <button v-on:click="removePlayer(idx)">Remove player</button>
      <hr/>
    </div>
    <button v-on:click="addTeam">Add Team</button>
    <button v-on:click="removeTeam">Remove Team</button>
    <button v-on:click="createGame">Create Game</button>
  </div>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';

const createTeam = (name) => ({ name, players: [{ name: 'Player 1' }] });

@Component
export default class NewGame extends Vue {
  games = ['Game 1', 'Game 2'];

  teams = [createTeam('Team 1'), createTeam('Team 2')];

  ncards = 5;

  createGame() {
    console.log(this.ncards, this.teams[0].name);
  }

  addTeam() {
    const { teams } = this;
    teams.push(createTeam(`Team ${teams.length + 1}`));
  }

  removeTeam() {
    const { teams } = this;
    if (teams) {
      teams.pop();
    }
  }

  addPlayer(teamIdx) {
    const { players } = this.teams[teamIdx];
    players.push({ name: `Player ${players.length + 1}` });
  }

  removePlayer(teamIdx) {
    const { players } = this.teams[teamIdx];
    if (players) {
      players.pop();
    }
  }
}
</script>
