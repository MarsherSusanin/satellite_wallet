<template>
  <div id="send">
    <Header />
    <div v-if="step === 1">
      <div class="out">
        <label>
          token
          <select v-model="walletOut">
            <option
              v-for="(wallet, index) in wallets"
              v-bind:key="index"
              :value="wallet.address"
            >{{wallet.suffix}} ({{wallet.name}})</option>
          </select>
        </label>
        <label>
          amount
          <input v-model="count"  />
        </label>
      </div>
      <div class="in">
        <label>
          recipient
          <input v-model="recipient" name="res" placeholder="enter address here..." />
        </label>
      </div>
    </div>
    <div v-if="step === 2">
      <section class="description">
        <h1>define fee</h1>
        <p>By default system offers you optimal gas price based on average value within last hour transactions.
        <br><br>
        You can choose custom value to perform transaction faster, or make it cost less.</p>
      </section>
      <section class="gas">
        <label>
          fee price
          <input v-model="fee" />
        </label>
        <button
            class="button button__inverse"
          >set optimal</button>
      </section>
    </div>
    <div v-if="step === 3">
      <section class="details">
        <h5>details</h5>
        <div class="content">
          <dl>
            <dt>current balance</dt><dd>0 {{selectedWallet.suffix}}</dd><br>
            <dt>transaction</dt><dd>{{ count }} {{selectedWallet.suffix}}</dd><br>
            <dt>fee price</dt><dd>{{ fee }} {{selectedWallet.suffix}}</dd><br>
            <dt>total balance</dt><dd>{{ 0 - count - fee }} {{selectedWallet.suffix}}</dd>
          </dl>
        </div>
      </section>
      <section class="details">
        <h5>recipient</h5>
        <div class="content">
          {{recipient}}
        </div>
      </section>
    </div>
    <section class="button-block">
      <button
        class="button button__main"
        :disabled="recipient.length === 0"
        v-on:click="sendHandler"
      >continue</button>
    </section>

  </div>
</template>

<script>
import Header from '../components/Header'

export default {
  name: 'Send',
  components: {
    Header
  },
  data () {
    return {
      wallets: [],
      walletOut: '',
      count: 0.00000,
      recipient: '',
      fee: 0,
      step: 1
    }
  },
  methods: {
    sendHandler () {
      this.step++
      if (this.step === 4) {
        this.$store.dispatch('sendTokens', {
          user_id: this.$store.state.user.user_id,
          session_id: this.$store.state.user.session_id,
          address_from: this.selectedWallet.address,
          private_key: this.selectedWallet.private_key,
          address_to: this.recipient,
          count_Tokens: this.count,
          fee: this.fee
        })
          .then(() => {
            this.$router.push('/')
          })
      }
    }
  },
  computed: {
    selectedWallet () {
      return this.wallets.find((wallet) => wallet.address === this.walletOut)
    }
  },
  mounted () {
    if (!this.$store.state.user) {
      this.$router.push('/create')
    } else {
      this.$store.dispatch('loadWallets')
      this.wallets = this.$store.state.wallets
      this.walletOut = this.wallets[0].address
    }
  }
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

#send{
  .out{
    margin-top: 80px;
    display: flex;

    label{
      flex-grow: 1;
    }
  }

  .gas{
    margin-top: 40px;
    display: flex;

    label{
      width: 80%
    }

    button{
      margin-top: 37px;
    }
  }

  .details{
    margin-top: 80px;
    border: 1px solid $color_text;
    margin-bottom: -50px;

    h5{
      color: $color_text;
      font-size: 14px;
      margin: 10px;
    }

    .content{
      border-top: 1px solid $color_text;
      padding: 10px;
      position: relative;

      dt, dd{
        display: inline;
      }

      dt{
        font-weight: 700;
        line-height: 30px;
      }

      dd{
        position: absolute;
        left: 200px;
        line-height: 30px
      }
    }
  }

  .description{
      display: flex;
      margin-top: 25%;

      h1{
        font-size: 12px;
        width: 160px;
      }

      p{
        margin-top: -1px;
        line-height: 17px;
        padding-left: 10px;
      }
    }

  select {
    width: 100%;
    background-color: transparent;
    border: 1px solid $color_text;
    color: $color_text;
    padding: 10.5px;
    margin-top: 7px;
    position: relative;
  }

   .button-block{
    position: absolute;
    bottom: 10px;
    width: calc(100%);
  }
}
</style>
