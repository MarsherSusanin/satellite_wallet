<template>
    <div id="login">
      <Logo />
      <section class="description">
        <h1>log in <br>procedure</h1>
      </section>
      <section class="input-block">
        <TextInput
          v-for="(data, index) in formData"
          v-bind:key="index"
          v-bind:data="data"
          v-on:input="inputHandler"
        />
        <button
          class="button button__main"
          v-on:click="loginHandler"
        >log in</button>
      </section>
      <footer>
        Don’t have your satellite wallet yet? <router-link class="accent" to="/create">Sign in</router-link>
      </footer>
    </div>
</template>

<script>
import Logo from '../components/Logo'
import TextInput from '../components/TextInput'

export default {
  name: 'Home',
  components: {
    Logo,
    TextInput
  },
  data () {
    return {
      formData: [
        {
          label: 'login',
          value: '',
          type: 'default',
          message: ''
        },
        {
          label: 'password',
          value: '',
          type: 'default',
          message: ''
        }
      ]
    }
  },
  methods: {
    loginHandler () {
      const data = this.formData.reduce((acc, input) => {
        acc[input.label] = input.value
        return acc
      }, {})
      this.$store.dispatch('login', data)
        .then(() => {
          this.$router.push('/')
        })
    },
    inputHandler (e) {
      const label = e.target.getAttribute('name')
      const inputData = this.formData.find(input => input.label === label)
      inputData.value = e.target.value
    }
  }
}
</script>

<style lang="scss">
#login{
  .description{
    display: flex;
    margin-top: 35%;

    h1{
      font-size: 12px;
      width: 160px;
    }
  }

  .input-block{
    margin-top: 40px;
  }

  footer{
    position: fixed;
    bottom: 10px;
  }
}
</style>
