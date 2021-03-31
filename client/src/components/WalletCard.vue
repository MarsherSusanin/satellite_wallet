<template>
    <div class="wallet-card">
      <div class="icon">
        <div class="coin-ico">
          <img v-if="data.name == 'cosmos'" src="../assets/cosmos.png">
          <img v-if="data.name == 'kava'" src="../assets/kava.png">
        </div>
      </div>
      <div class="content">
        <div class="head"><h2>{{data.name}}</h2><span class="course course--up">+26.0543$</span></div>
        <div class="value">
          <div class="dollar">0 $</div>
          <div class="coin">0.00000 {{data.suffix}}</div>
        </div>
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
      display: flex;
      justify-content: center;
      padding: 10px;
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
        display: inline;
      }

      .course{
        text-align: right;
        float: right;

        &--up{
          color: $color_success;
        }
      }
    }

    .value{
      display: flex;

      .dollar{
        padding: 5px 10px;
        border-right: 1px solid $color_text;
        flex-grow: 1;
        font-size: 12px;
      }

      .coin{
        padding: 5px 10px;
        flex-grow: 1;
        font-size: 12px;
      }
    }
  }
}
</style>
