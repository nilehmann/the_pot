<template>
  <div class="add-cards" v-if="cards">
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
      <div class="container cards">
        <div v-for="(card, idx) in cards" :key="idx">
          <b-input
            type="textarea"
            v-model="card.text"
            class="text"/>
        </div>
        <div class="actions">
          <b-button v-on:click="send" class="is-primary">Send</b-button>
        </div>
      </div>
    </div>
    <b-loading
      :is-full-page="true"
      :active.sync="isLoading"
      :can-cancel="false"/>
  </div>
</template>

<script>
import { Component, Prop, Vue } from 'vue-property-decorator';
import axios from 'axios';

@Component
export default class Games extends Vue {
  @Prop(String) gameId;

  maxCards = 0;

  cards = null;

  isLoading = false;

  get playerId() {
    return this.$route.query.playerId;
  }

  mounted() {
    this.isLoading = true;
    axios
      .get(`http://localhost:5000/games/${this.gameId}/cards?playerId=${this.playerId}`)
      .then((response) => this.updateCards(response))
      .catch(this.errorAlert);
  }

  send() {
    if (this.isLoading) {
      return;
    }
    this.isLoading = true;
    axios
      .post(`http://localhost:5000/games/${this.gameId}/cards`, {
        playerId: this.playerId,
        cards: this.cards,
      })
      .then((response) => this.updateCards(response))
      .catch(this.errorAlert);
  }

  updateCards(response) {
    this.isLoading = false;
    this.maxCards = response.data.max_cards;
    this.cards = response.data.cards;
    const n = this.maxCards - this.cards.length;
    for (let i = 0; i < n; i += 1) {
      this.cards.push({});
    }
  }

  errorAlert(error) {
    this.isLoading = false;
    console.log(error);
    this.$buefy.dialog.alert('There was an error');
  }
}
</script>

<style scoped lang="scss">
  .cards {
    width: 500px;
  }

  .text {
    margin-bottom: 20px;
  }

  .actions {
    display: flex;
    justify-content: flex-end;
  }
</style>

<style lang="scss">
.add-cards textarea {
  min-height: 70px !important;
}
</style>
