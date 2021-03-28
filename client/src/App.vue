<template>
  <div id="app">
    <Preloader>
      <router-view/>
    </Preloader>
    <Message
      v-if="allert.isActive"
      v-bind:type="allert.type"
      v-bind:title="allert.title"
      v-on:close="closeAlertHandler"
    >{{ allert.text }}</Message>
  </div>
</template>

<script>
import Message from './components/Message'
import Preloader from './components/Preloader'

export default {
  components: {
    Message,
    Preloader
  },
  computed: {
    allert () { return this.$store.state.allert }
  },
  methods: {
    closeAlertHandler () {
      this.$store.commit('closeAllert')
    }
  }
}
</script>

<style lang="scss">
  @import './assets/scss/styles';
</style>
