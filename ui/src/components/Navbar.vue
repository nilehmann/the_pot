<template>
  <b-navbar id="nav" class="is-spaced has-shadow" wrapper-class="container">
    <template slot="brand">
      <b-navbar-item tag="router-link" to="/">
        <img src="/logo.webp"> The Pot
      </b-navbar-item>
    </template>
    <template slot="end">
      <b-navbar-item tag="div">
        <a class="button" v-on:click="$router.go(-1)">
          <strong>Back</strong>
        </a>
      </b-navbar-item>
    </template>
  </b-navbar>
</template>
