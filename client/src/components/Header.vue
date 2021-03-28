<template>
  <header class="header">
    <button class="back"><img src="../assets/back.png"></button>
    <h1 class="app-name">satellite</h1>
  </header>
</template>

<script>
export default {
  name: 'Header'
}
</script>

<style lang="scss">
  @import '../assets/scss/_variables';

  .header{
    display: flex;
    border: 1px solid $color_text;
    position: absolute;
    top: 0;
    left: 0;
    padding: 10px;
    width: 100%;

    .app-name{
      color: $color_text;
      text-align: center;
      width: 100%;
      margin-left: -22px;
    }

    .back{
      background-color: transparent;
      border: none;
    }
  }
</style>
