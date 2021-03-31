<template>
  <ol class="navigation">
    <li class="navigation__item navigation__item--current">
      <img src="../assets/main.png" />
      <h5>main</h5>
    </li>
    <li class="navigation__item">
      <img src="../assets/transactions.png" />
      <h5>transactions</h5>
    </li>
    <li class="navigation__item">
      <img src="../assets/settings.png" />
      <h5>settings</h5>
    </li>
  </ol>
</template>

<script>
export default {
  name: 'Menu'
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

.navigation{
  position: absolute;
  top: 50px;
  left: 0;
  display: flex;
  justify-content: center;
  border: 1px solid $color_text;
  border-right: none;
  width: 100%;

  &__item{
    padding: 11px 10px;
    border-right: 1px solid $color_text;
    flex-grow: 1;
    opacity: .6;
    text-align: center;

    h5{
      color: $color_text;
    }

    &::marker {
      content: '';
    }

    &--current{
      opacity: 1;
    }

    &--disabled{
      opacity: 1;
      background: $color_text;
      color: $color_background;
    }
  }
}
</style>
