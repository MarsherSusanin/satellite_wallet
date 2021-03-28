<template>
    <div class="seed-loader">
        <div class="screen">
            <h5>satellite security system v 1.33.7</h5>
            <div class="msg" v-if="loadingString">
                <h5>loading...</h5>
                {{ loadingString }}
            </div>
            <div
                class="msg"
                v-for="(text, index) in messages"
                v-bind:key="index"
            >
                <h5>adm:</h5>
                {{ text }}
            </div>
        </div>
        <button
            class="button button__main"
            v-on:click="buttonHandler"
        >view seed phrase</button>
    </div>
</template>

<script>

export default {
  name: 'SeedLoader',
  data () {
    return {
      loadingString: '',
      messages: []
    }
  },
  methods: {
    buttonHandler () {
      const progress = this.emulateLoading()
      this.$emit('load', progress)
    },
    emulateLoading () {
      return new Promise(resolve => {
        const messages = [
          'Look around and remember:',
          'Big Brother always watching',
          'for you'
        ]
        const timer = setInterval(() => {
          this.loadingString += '/'
          if (this.loadingString.length % 9 === 0) {
            this.messages.push(messages[(this.loadingString.length / 9) - 1])
          }
          if (this.loadingString.length >= 27) {
            clearInterval(timer)
            resolve()
          }
        }, 120)
      })
    }
  }
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

.seed-loader{
    .screen{
        height: 230px;
        background-color: $color_main;
        padding: 30px;
        color: $color_background;

        .msg{
          margin-top: 20px;
        }

        h5{
            color: $color_background;
            display: inline;
        }
    }
}
</style>
