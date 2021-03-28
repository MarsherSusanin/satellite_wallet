<template>
  <div id="preloader">
    <template v-if="isLoading">
      <div class="wrapper">
        <img src="../assets/preloader.gif" />
      </div>
    </template>
    <template v-else>
      <slot></slot>
    </template>
  </div>
</template>

<script>
export default {
  name: 'Preloader',
  computed: {
    isLoading () { return this.$store.state.isLoading }
  }
}
</script>

<style lang="scss">
#preloader {
  .wrapper{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
}
</style>
