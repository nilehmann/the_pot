<template>
  <div class="play">
    <Keypress :key-code="32" event="keyup" @pressed="keyPressed" />
    <b-navbar id="nav" class="is-spaced has-shadow" wrapper-class="container">
      <template slot="brand">
        <b-navbar-item tag="router-link" to="/">
          <img src="/logo.webp">
        </b-navbar-item>
      </template>
      <template slot="end">
        <b-navbar-item tag="div">
          <a class="button is-primary" v-on:click="$router.go(-1)">
            <strong>Back</strong>
          </a>
        </b-navbar-item>
      </template>
    </b-navbar>
    <div class="section">
      <div v-if="state == 'stopped'" class="container">
        <b-button v-on:click="start" class="is-large start" :disabled="isLoading">
          Start
        </b-button>
      </div>
      <div v-else-if="card && state == 'started'" class="container">
        <b-message class="card">
          {{card.text}}
        </b-message>
        <div class="buttons">
          <b-button v-on:click="stop" :disabled="isLoading">Stop</b-button>
          <b-button v-on:click="next" :disabled="isLoading">Next</b-button>
        </div>
      </div>
      <div v-else class="container">
        There are no more cards
      </div>
    </div>
  </div>
</template>

<script>
import { Component, Vue, Prop } from 'vue-property-decorator';
import Keypress from 'vue-keypress';
import axios from 'axios';

const Components = Vue.extend({
  components: { Keypress },
});

@Component
export default class Play extends Components {
  @Prop(String) gameId

  card = null

  state = 'stopped'

  isLoading = false

  keyPressed() {
    if (this.state === 'stopped') {
      this.start();
    } else if (this.state === 'started') {
      this.next();
    }
  }


  start() {
    if (this.isLoading || this.state !== 'stopped') {
      return;
    }
    this.isLoading = true;
    axios
      .get(`http://localhost:5000/games/${this.gameId}/draw`)
      .then(this.updateCard);
  }

  next() {
    if (this.isLoading || this.state !== 'started' || !this.card) {
      return;
    }
    this.isLoading = true;
    axios
      .post(`http://localhost:5000/games/${this.gameId}/guess`, {
        playerId: this.playerId,
        cardId: this.card.id,
      })
      .then(this.updateCard)
      .catch(this.errorAlert);
  }

  stop() {
    this.state = 'stopped';
  }

  get playerId() {
    return this.$route.query.playerId;
  }

  updateCard(response) {
    if (!response.data.card) {
      this.state = 'finished';
    } else {
      this.state = 'started';
      this.card = response.data.card;
    }
    this.isLoading = false;
  }

  errorAlert(error) {
    this.isLoading = false;
    console.log(error);
    this.$buefy.dialog.alert('There was an error');
  }
}

</script>

<style scoped lang="scss">
  .container {
    display: flex;
    justify-content: center;
    padding-top: 100px;
    flex-direction: column;
    align-items: center;
  }

  .card {
    width: 500px;
    min-height: 70px;
  }
</style>
