<template>
  <label>
    <div
      class="checkbox"
      v-bind:class="{
        checked: value,
        disabled: data.disabled
      }"
      v-on:click="clickHandler"
    ></div>
    <input
      type="hidden"
      :name="data.label"
      :value="data.value"
      :checked="value"
      :disabled="data.disabled"
    />
    {{ data.label }}
  </label>
</template>

<script>
export default {
  name: 'CheckboxInput',
  props: { data: Object, value: Boolean },
  methods: {
    clickHandler () {
      this.$emit('click')
    }
  }
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

label{
  line-height: 20px;

  .checkbox{
    width: 20px;
    height: 20px;
    border: 1px solid $color_main;
    display: inline-block;
    position: relative;
    bottom: -6px;
    margin-right: 10px;
  }

  .checkbox.checked{
    background-image: url('~@/assets/checkbox_default.png');
    background-position: -1px -1px;
  }

  .checkbox.disabled{
    background: $color_text;
    border-color: $color_background;
    opacity: .6;
  }

  .checkbox.disabled.checked{
    background-image: url('~@/assets/checkbox_disabled.png');
    background-position: -1px -1px;
  }
}
</style>
