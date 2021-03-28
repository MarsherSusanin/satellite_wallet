<template>
    <div class="wallet-card">
      <div class="icon">
        <div class="coin-ico"></div>
      </div>
      <div class="content">
        <div class="head"><h2>{{data.name}}</h2></div>
        <div class="value">{{data.value}}</div>
      </div>
    </div>
</template>

<script>
export default {
  name: 'WalletCard',
  props: {
    data: Object
  }
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

.wallet-card{
  display:flex;
  border: 1px solid $color_text;
  margin-bottom: 20px;
  height: 60px;

  .icon{
    padding: 5px;
    border-right: 1px solid $color_text;

    .coin-ico{
      background-color: $color_text;
      width: 50px;
      height: 50px;
      border-radius: 6px;
      margin: auto;
    }
  }

  .content{
    display: flex;
    flex-direction: column;
    width: 100%;

    .head{
      border-bottom: 1px solid $color_text;
      padding: 5px 10px;

      h2{
        font-size: 12px;
        color: $color_text;
      }
    }

    .value{
      padding: 5px 10px;
    }
  }
}
</style>
