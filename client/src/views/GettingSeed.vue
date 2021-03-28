<template>
  <div id="get-seed">
    <Message
      v-if="isAlertActive"
      v-bind:type="'default'"
      v-bind:title="'warning'"
      v-on:close="closeAlertHandler"
    >
      <p>Protect your seed phrase! Loss of a phrase is a loss of access to wallet</p>

      <checkbox-input
        v-bind:data="{
          label: 'confirm and totally understand',
          value: 1,
          disabled: false
        }"
        v-on:click="agreeHandler"
        v-model="isAgree"
      />
    </Message>
    <Header />
    <Navigation
      v-bind:items="navigation"
    />
    <p class="description">
      Write down, or copy your seed phrase
    </p>
    <section class="input-block">
      <SeedLoader
        v-if="!seed"
        v-on:load="loadHandler"
      />
      <SeedViewer
        v-if="seed && !isAgree"
        v-bind:seed="seed"
      />
    </section>
    <section class="button-block">
      <button
        class="button button__main"
        v-on:click="continueHandler"
        :disabled="!seed"
      >continue</button>
    </section>
  </div>
</template>

<script>
import Header from '../components/Header'
import Navigation from '../components/Navigation'
import SeedLoader from '../components/SeedLoader'
import SeedViewer from '../components/SeedViewer'
import Message from '../components/Message'
import CheckboxInput from '../components/CheckboxInput'

export default {
  components: {
    Header,
    Navigation,
    SeedLoader,
    SeedViewer,
    Message,
    CheckboxInput
  },
  data () {
    return {
      navigation: [
        { title: 'create login/passwd', type: 'disabled' },
        { title: 'seed phrase generation', type: 'current' },
        { title: 'confirm seed phrase', type: 'default' }
      ],
      seed: '',
      isAlertActive: false,
      isAgree: false
    }
  },
  methods: {
    continueHandler () {
      this.isAlertActive = true
    },
    closeAlertHandler () {
      this.isAlertActive = false
    },
    agreeHandler () {
      this.isAgree = true
      this.isAlertActive = false
      this.$router.push('/confirm-seed')
    },
    loadHandler (loadingProgress) {
      console.log(loadingProgress)
      Promise.all([
        loadingProgress,
        this.$store.dispatch('getSeed')
      ])
        .then(([, { mnemonic }]) => {
          this.seed = mnemonic
        })
    }
  }
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

#get-seed{
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
