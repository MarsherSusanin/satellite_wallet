<template>
  <div id="confirm-seed">
    <Header />
    <Navigation
      v-bind:items="navigation"
    />
    <p class="description">
      select each word in order it was presented on previous step
    </p>
    <section class="input-block">
        <SeedInput
            v-bind:seed="seed"
            v-on:input="inputHandler"
        />
    </section>
    <section class="button-block">
      <button
        class="button button__main"
        v-on:click="sendHandler"
      >continue</button>
    </section>
  </div>
</template>

<script>
import Header from '../components/Header'
import Navigation from '../components/Navigation'
import SeedInput from '../components/SeedInput'

export default {
  components: {
    Header,
    Navigation,
    SeedInput
  },
  data () {
    return {
      navigation: [
        { title: 'create login/passwd', type: 'disabled' },
        { title: 'seed phrase generation', type: 'disabled' },
        { title: 'confirm seed phrase', type: 'current' }
      ],
      seed: '',
      userSeed: ''
    }
  },
  methods: {
    inputHandler (data) {
      this.userSeed = data
    },
    sendHandler () {
      if (this.seed === this.userSeed) {
        this.$store.dispatch('createWallets')
          .then(() => this.$router.push('/'))
      }
    }
  },
  mounted () {
    console.log(this.$store.state.mnemonic)
    this.seed = this.$store.state.mnemonic
  }
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

#confirm-seed{
  .description{
    margin-top: 145px;
  }

  .input-block{
    margin-top: 40px;
  }

  .button-block{
    position: fixed;
    bottom: 10px;
    width: calc(100% - 20px);
    background: $color_background;
  }
}
</style>
