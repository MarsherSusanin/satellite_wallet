<template>
  <div id="registration">
    <Header />
    <Navigation
      v-bind:items="navigation"
    />
    <p class="description">
      Create login and password to log in your SATELLITE wallet on this device.
    </p>
    <section class="input-block">
      <TextInput
        v-for="(data, index) in formData"
        v-bind:key="index"
        v-bind:data="data"
        v-on:input="inputHandler"
      />
    </section>
    <section class="agree">
      <checkbox-input
        v-bind:data="{
          label: 'I was informed that SATELLITE wouldn’t be able to restore password in case of loss.',
          value: 1,
          disabled: false
        }"
        v-on:click="agreeHandler"
        v-model="isAgree"
      />
    </section>
    <section class="button-block">
      <button
        class="button button__main"
        :disabled="isFormCorrect"
        v-on:click="sendHandler"
      >create wallet</button>
    </section>
  </div>
</template>

<script>
import Header from '../components/Header'
import Navigation from '../components/Navigation'
import TextInput from '../components/TextInput'
import CheckboxInput from '../components/CheckboxInput'

import { validatePass } from '../common/registration'

export default {
  components: {
    Header,
    Navigation,
    TextInput,
    CheckboxInput
  },
  data () {
    return {
      navigation: [
        { title: 'create login/passwd', type: 'current' },
        { title: 'seed phrase generation', type: 'default' },
        { title: 'confirm seed phrase', type: 'default' }
      ],
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
        },
        {
          label: 'password confirmation',
          value: '',
          type: 'default',
          message: ''
        }
      ],
      isAgree: false
    }
  },
  methods: {
    sendHandler () {
      const data = this.formData.reduce((acc, input) => {
        acc[input.label] = input.value
        return acc
      }, {})
      this.$store.dispatch('registration', data)
        .then(() => this.$router.push('/get-seed'))
    },
    agreeHandler () {
      this.isAgree = !this.isAgree
    },
    inputHandler (e) {
      const label = e.target.getAttribute('name')
      const inputData = this.formData.find(input => input.label === label)
      inputData.value = e.target.value

      if (label === 'password') {
        this.checkPassword(e.target.value)
        this.checkPasswordConfirm()
      }

      if (label === 'password confirmation') {
        this.checkPasswordConfirm()
      }
    },
    checkPassword (pass) {
      const validation = validatePass(pass)
      const inputData = this.formData.find(input => input.label === 'password')
      inputData.type = validation.type
      inputData.message = validation.message
    },
    checkPasswordConfirm () {
      const inputPass = this.formData.find(input => input.label === 'password')
      const inputConfirm = this.formData.find(input => input.label === 'password confirmation')

      if (inputPass.value !== inputConfirm.value) {
        inputConfirm.type = 'error'
        inputConfirm.message = 'password don`t equal'
      } else {
        inputConfirm.type = 'success'
        inputConfirm.message = ''
      }
    }
  },
  computed: {
    isFormCorrect () {
      return ![
        () => this.isAgree,
        () => this.formData.reduce((acc, data) => data.value.length > 0 && acc, true),
        () => this.formData.reduce((acc, data) => !(data.type === 'error') && acc, true)
      ].reduce((acc, validator) => validator() && acc, true)
    }
  }
}
</script>

<style lang="scss">
#registration{
  .description{
    margin-top: 145px;
  }

  .input-block{
    margin-top: 40px;
  }

  .agree{
    margin-top: 40px;
  }

  .button-block{
    position: fixed;
    bottom: 10px;
    width: calc(100% - 20px);
  }
}
</style>
