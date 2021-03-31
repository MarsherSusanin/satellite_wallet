<template>
  <div class="total">
    <h3>total balance:</h3>
    <div class="dollars">
      <div class="value">1234566543 $</div>
      <div class="icon">
        <img src="../assets/total.png" />
      </div>
    </div>
    <div class="change">
      last 24h: <span class="up">+2.00765 $</span>
    </div>
    <nav>
      <button v-on:click="sendHandler" class="button button__inverse">send</button>
      <button class="button button__inverse">receive</button>
      <button style="border-right: none" class="button button__inverse">exchange</button>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'Total',
  methods: {
    sendHandler () { this.$router.push('/send') }
  }
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

.total{
  margin: 40px 0;
  border: 1px solid $color_main;

  h3{
    color: $color_text;
    margin: 10px;
  }

  .dollars{
    border-top: 1px solid $color_main;
    display: flex;

    .value{
      font-size: 24px;
      padding: 15px 10px;
      border-right: 1px solid $color_main;
      flex-grow: 1;
    }

    .icon{
      text-align: center;
      display: flex;
      justify-content: center;
      align-items: center;
      width: 65px;
    }
  }

  .change{
    border-top: 1px solid $color_main;
    padding: 10px;
    font-weight: 700;

    .up{
      color: $color_success;
    }
  }

  nav{
    display: flex;

    button{
      margin-bottom: 0;
      border-bottom: none;
      border-left: none;
    }
  }
}
</style>
