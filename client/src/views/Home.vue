<template>
  <div class="home">
    <Header />
    <Total />
    <WalletCard
      v-for="(wallet, index) in wallets"
      v-bind:key="index"
      v-bind:data="wallet"
    />
    <div class="footer">
      <Menu />
    </div>
  </div>
</template>

<script>
import Total from '../components/Total'
import Header from '../components/Header'
import WalletCard from '../components/WalletCard'
import Menu from '../components/Menu'

export default {
  name: 'Home',
  components: {
    Header,
    WalletCard,
    Menu,
    Total
  },
  data () {
    return {
      wallets: []
    }
  },
  mounted () {
    if (!this.$store.state.user) {
      this.$router.push('/create')
    } else {
      this.$store.dispatch('loadWallets')
      this.wallets = this.$store.state.wallets
    }
  }
}
</script>

<style lang="scss">
.home{
  padding-top: 60px;
  height: calc(100vh - 50px);
  position: relative;

  .footer{
    position: absolute;
    bottom: 0px;
    left: 0px;
    width: 100%;
    height: 60px;
  }
}
</style>
