<template>
  <div class="home">
    <Logo />
    {{ balance }}
  </div>
</template>

<script>
import Logo from '../components/Logo'
import axios from 'axios'

export default {
  name: 'Home',
  components: {
    Logo
  },
  data () {
    return {
      wallets: [],
      balance: []
    }
  },
  mounted () {
    if (!this.$store.state.user) {
      this.$router.push('/create')
    }
    this.$store.dispatch('loadWallets')
    this.wallets = this.$store.state.wallets
    Promise.all(this.wallets.map(wallet => axios({
      method: 'post',
      url: 'http://35.184.30.28/api/1.0/getbalans/',
      data: {
        user_id: this.$store.state.user.user_id,
        session_id: this.$store.state.user.session_id,
        address: wallet.address
      }
    })))
      .then(data => {
        this.balance = data.map(item => item.data)
      })
  }
}
</script>

<style lang="scss">

</style>
