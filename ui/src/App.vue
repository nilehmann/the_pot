<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style lang="scss">
  @import "~bulma/sass/utilities/_all";

  $primary: #00d1b2;
  $primaryInvert: findColorInvert($primary);
  $success: #48c774;
  $successInvert: findColorInvert($success);
  $warning: #ffdd57;
  $warningInvert: findColorInvert($warning);

  $colors: (
    "white": ($white, $black),
    "black": ($black, $white),
    "light": ($light, $light-invert),
    "dark": ($dark, $dark-invert),
    "primary": ($primary, $primary-invert),
    "info": ($info, $info-invert),
    "success": ($success, $success-invert),
    "warning": ($warning, $warning-invert),
    "danger": ($danger, $danger-invert),
  );

  $link: $primary;
  $link-invert: $primary-invert;
  $link-focus-border: $primary;

  @import "~bulma";
  @import "~buefy/src/scss/buefy";

  .progress.is-tiny {
    height: 0.6rem;
  }
</style>
