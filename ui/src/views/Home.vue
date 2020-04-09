<template>
  <div id="home">
    <b-navbar id="nav" class="is-spaced has-shadow" wrapper-class="container">
      <template slot="brand">
        <b-navbar-item tag="router-link" to="/">
          <img src="/logo.webp"> The Pot
        </b-navbar-item>
      </template>
      <template slot="end">
        <b-navbar-item>
          <router-link tag="button" to="/new" class="button is-primary">
            New Game
          </router-link>
        </b-navbar-item>
      </template>
    </b-navbar>
    <div class="section">
      <div class="container">
        <router-view/>
      </div>
    </div>
  </div>
</template>
