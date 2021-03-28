<template>
  <div id="create-page">
    <Logo />
    <section class="description">
      <h1>wallet setup</h1>
      <p>import an existing wallet or create a new one</p>
    </section>
    <section class="buttons">
      <button class="button button__inverse">import</button>
      <button class="button button__main" v-on:click="createHandler">create</button>
    </section>
    <section class="terms">
      by proceeding, you agree to next <a>Terms & Conditions</a>
    </section>
    <footer class="log-in">
      Already have your satellite wallet? <router-link class="accent" to="/login">Log in</router-link>
    </footer>
  </div>
</template>

<script>
import Logo from '../components/Logo'

export default {
  components: {
    Logo
  },
  methods: {
    createHandler () {
      this.$router.push('/registration')
    }
  }
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

  #create-page{

    .description{
      display: flex;
      margin-top: 35%;

      h1{
        font-size: 12px;
        width: 160px;
      }

      p{
        margin-top: -1px;
        line-height: 17px;
      }
    }

    .buttons{
      margin-top: 10%;
    }

    .terms{
      font-size: 10px;
      margin-top: 4%;

      a{
        font-size: 10px;
      }
    }

    footer{
      position: absolute;
      bottom: 10px;
      width: 100%;
      background: $color_background;
    }

  }
</style>
