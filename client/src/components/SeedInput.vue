<template>
    <div class="seed-input">
        <div class="screen">
            <div
              class="word"
              v-for="(word, index) in buildedArray"
              v-bind:key="index"
            > {{ index }}. {{ word }} </div>
        </div>
        <div class="heap">
          <div
              class="word"
              v-for="(word, index) in seedArray"
              v-bind:key="index"
              v-on:click="addWordHandler"
              :data-word="word"
            > {{ word }} </div>
        </div>
    </div>
</template>

<script>

export default {
  name: 'SeedLoader',
  data () {
    return {
      buildedArray: []
    }
  },
  props: {
    seed: String
  },
  methods: {
    addWordHandler (e) {
      const word = e.target.dataset.word
      const index = this.seedArray.findIndex((item) => item === word)
      this.buildedArray.push(word)
      this.seedArray.splice(index, 1)

      this.$emit('input', this.buildedArray.join(' '))
    }
  },
  computed: {
    seedArray () { return this.seed.split(' ').sort(() => Math.random() - 0.5) }
  }
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

.seed-input{
    .screen{
      padding: 30px;
      border: 1px solid $color_main;
      display: flex;
      flex-wrap: wrap;
    }

    .heap{
      display: flex;
      flex-wrap: wrap;
      padding: 20px 0;
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
