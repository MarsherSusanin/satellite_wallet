<template>
  <ol class="navigation">
    <li
      v-for="(item, index) in items"
      v-bind:key="index"
      v-bind:class="[
        'navigation__item',
        item.type === 'disabled' ? 'navigation__item--disabled' :
        item.type === 'current' ? 'navigation__item--current' : ''
      ]"
    >{{ index }} {{ item.title }}</li>
  </ol>
</template>

<script>
export default {
  name: 'Navigation',
  props: {
    items: Array
  }
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
