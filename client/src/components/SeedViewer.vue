<template>
    <div class="seed-viewer">
        <div class="screen">
            <div
              class="word"
              v-for="(word, index) in seedArray"
              v-bind:key="index"
            > {{ index }}. {{ word }} </div>
        </div>
        <button
            class="button button__inverse"
            v-on:click="buttonHandler"
        >copy seed phrase</button>
    </div>
</template>

<script>

export default {
  name: 'SeedLoader',
  props: {
    seed: String
  },
  methods: {
    buttonHandler () {
      navigator.clipboard.writeText(this.seed)
        .then(() => {
          this.$store.commit('showAllert', { type: 'success', title: 'success', text: 'Seed copied to clipboard' })
        })
        .catch(() => {
          this.$store.commit('showAllert', { type: 'error', title: 'error', text: 'Error!' })
        })
    }
  },
  computed: {
    seedArray () {
      return this.seed.split(' ')
    }
  }
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

.seed-viewer{
    .screen{
        padding: 30px;
        border: 1px solid $color_main;
        display: flex;
        flex-wrap: wrap;
        margin-bottom: 0;
        border-bottom: none;
    }

    .word{
      border: 1px solid $color_main;
      margin: 5px;
      padding: 5px;
    }

    button{
      margin-top: 0;
      margin-bottom: 60px;
    }
}

</style>
