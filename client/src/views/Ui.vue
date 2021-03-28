<template>
  <div class="uikit">
    <h1>UI KIT</h1>

    <table>
      <tr>
        <td><h2>Logo</h2></td>
        <td class="content">
          <logo />
        </td>
      </tr>
      <tr>
        <td><h2>Text input</h2></td>
        <td class="content">
          <text-input
            v-bind:data="{
              label: 'label',
              value: 'Text Input',
              type: 'default',
              message: ''
            }"
          />
          <text-input
            v-bind:data="{
              label: 'label',
              value: 'Text Input',
              type: 'success',
              message: 'SUCCESS: message'
            }"
          />
          <text-input
            v-bind:data="{
              label: 'label',
              value: 'Text Input',
              type: 'warning',
              message: 'WARNING: message'
            }"
          />
          <text-input
            v-bind:data="{
              label: 'label',
              value: 'Text Input',
              type: 'error',
              message: 'ERROR: message'
            }"
          />
          <text-input
            v-bind:data="{
              label: 'label',
              value: 'Text Input',
              type: 'disabled',
              message: ''
            }"
          />
        </td>
      </tr>
      <tr>
        <td><h2>Checkboxes</h2></td>
        <td>
          <checkbox-input
            v-bind:data="{
              label: 'default',
              value: 1,
              checked: true,
              disabled: false
            }"
          />
          <checkbox-input
            v-bind:data="{
              label: 'disabled',
              value: 1,
              checked: true,
              disabled: true
            }"
          />
        </td>
        <tr>
        <td><h2>buttons</h2></td>
        <td>
          <button class="button button__main">button</button>
          <button class="button button__inverse">button</button>
          <button disabled class="button button__main">button</button>
          <button disabled class="button button__inverse">button</button>
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import Logo from '../components/Logo'
import TextInput from '../components/TextInput'
import CheckboxInput from '../components/CheckboxInput'

export default {
  components: {
    Logo,
    TextInput,
    CheckboxInput
  }
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

.uikit{
  width: 1000px;
  margin: 0 auto;

  table{
    border-collapse: collapse;

    td{
      padding: 0 15px;
      border: 2px solid $color_main;
    }

    .content{
      width: 700px;
    }
  }
}
</style>
