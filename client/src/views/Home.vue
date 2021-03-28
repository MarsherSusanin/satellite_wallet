<template>
  <div class="home">
    <Header />
    <WalletCard
      v-for="(wallet, index) in wallets"
      v-bind:key="index"
      v-bind:data="wallet"
    />
  </div>
</template>

<script>
import Header from '../components/Header'
import WalletCard from '../components/WalletCard'

export default {
  name: 'Home',
  components: {
    Header,
    WalletCard
  },
  data () {
    return {
      wallets: [
        { name: 'Kava', value: 0 },
        { name: 'Atom', value: 0 }
      ]
    }
  }
}
</script>

<style lang="scss">
.home{
  padding-top: 60px;
}
</style>
