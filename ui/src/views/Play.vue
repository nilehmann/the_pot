<template>
  <div class="play">
    <!-- Space -->
    <Keypress :key-code="32" event="keyup" @pressed="spacePressed" />
    <!-- Esc -->
    <Keypress :key-code="27" event="keyup" @pressed="stop" />
    <Navbar/>
    <div class="section">
      <div v-if="state == 'stopped'" class="container">
        <b-button
          v-on:click="start"
          class="is-large start"
          :disabled="isLoading"
        >
          Start
        </b-button>
      </div>
      <div v-else-if="card && state == 'started'" class="container">
        <div class="card-container">
          <b-message class="card">
            <strong>{{card.text}}</strong>
          </b-message>
        </div>
        <b-progress :value="timeLeft*100/maxTime" class="timer" size="is-tiny" />
        <div class="buttons">
          <b-button v-on:click="stop" :disabled="isLoading" class="is-medium">
            Stop
          </b-button>
          <b-button
            v-on:click="next"
            :disabled="isLoading"
            class="is-medium"
          >
            Next
          </b-button>
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

import Navbar from '../components/Navbar.vue';

@Component({ components: { Keypress, Navbar } })
export default class Play extends Vue {
  @Prop(String) gameId

  lastActionTime = null

  throttleMillis = 1000

  card = null

  state = 'stopped'

  isLoading = false

  timeLeft = 0;

  maxTime = 60;

  tickMilli = 100;

  spacePressed() {
    if (this.state === 'stopped') {
      this.start();
    } else if (this.state === 'started') {
      this.next();
    }
  }

  start() {
    if (this.shouldSkip('stopped')) {
      return;
    }

    this.setTimer();
    this.apiCall((ax) => ax.get(`${this.$API}/games/${this.gameId}/draw`));
  }

  next() {
    if (this.shouldSkip('started') || !this.card) {
      return;
    }
    this.apiCall((ax) => (
      ax.post(`${this.$API}/games/${this.gameId}/guess`, {
        playerId: this.playerId,
        cardId: this.card.id,
      })
    ));
  }

  shouldSkip(expectedState) {
    return this.isLoading || this.state !== expectedState || this.shouldThrottle();
  }

  stop() {
    if (this.interval) {
      clearInterval(this.interval);
    }
    this.lastActionTime = new Date();
    this.state = 'stopped';
  }

  setTimer() {
    this.timeLeft = this.maxTime;
    this.interval = setInterval(this.tick, this.tickMilli);
  }

  tick() {
    this.timeLeft -= this.tickMilli / 1000;
    if (this.timeLeft <= 0) {
      this.stop();
    }
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

  shouldThrottle() {
    const curr = new Date();
    if (this.lastActionTime && curr - this.lastActionTime <= this.throttleMillis) {
      return true;
    }
    return false;
  }

  errorAlert(error) {
    this.isLoading = false;
    console.log(error);
    this.$buefy.dialog.alert('There was an error');
  }

  apiCall(f) {
    this.isLoading = true;
    this.lastActionTime = new Date();
    f(axios).then(this.updateCard).catch(this.errorAlert);
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

  .card-container {
    width: 500px;
    min-height: 200px;
    margin-bottom: 50px;
  }

  .timer {
    width: 500px;
  }

  .card {
    font-size: 14pt;
  }
</style>
