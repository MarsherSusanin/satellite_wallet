<template>
  <label
    v-bind:class="[
      data.type === 'error' ? 'error' :
      data.type === 'warning' ? 'warning' :
      data.type === 'success' ? 'success' :
      data.type === 'disabled' ? 'disabled' : ''
    ]"
  >
    {{ data.label }}
    <input
      :name="data.label"
      :value="data.value"
      :disabled="data.type === 'disabled'"
      v-on:input="inputHandler"
      type="text"
    />
    <div v-if="data.message" class="message">{{ data.message }}</div>
  </label>
</template>

<script>
export default {
  name: 'TextInput',
  props: { data: Object },
  methods: {
    inputHandler (e) { this.$emit('input', e) }
  }
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

label{
  display: block;
  margin: 10px 0 20px 0;
}

input{
  font-family: 'Space Mono';
  font-size: 12px;
  padding: 0 10px;
  margin: 7px 0;
  height: 40px;
  width: 100%;
  color: $color_text;
  background-color: transparent;
  display: block;
  border: 1px solid $color_text;
}

input:focus{
  outline: none;
}

input:disabled{
  color: $color_background;
  background-color: $color_text;
  opacity: .6;
}

label.error{
  input{
    border-color: $color_error;
  }
  .message{
    color: $color_error;
  }
}

label.success{
  .message{
    color: $color_success;
  }
}

label.warning{
  .message{
    color: $color_warning;
  }
}
</style>
