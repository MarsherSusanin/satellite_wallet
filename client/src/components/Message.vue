<template>
  <div class="overlay">
    <div  v-bind:class="[
        'card',
        type === 'error' ? 'card--error' :
        type === 'success' ? 'card--success' : ''
      ]"
    >
      <div class="card__header">
        <h2>{{ title }}</h2>
        <button
          @click="closeHandler"
          class="card__close-btn"
        >&#215;</button>
      </div>
      <div class="card__body">
        <slot></slot>
      </div>
      <div
        @click="closeHandler"
        v-if="type === 'error' || type === 'success'"
        class="card__footer"
      >
        <h3>proceed {{ type === 'error' ? 'back' : 'forward' }}</h3>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Message',
  props: {
    type: String,
    title: String
  },
  methods: {
    closeHandler () { this.$emit('close') }
  }
}
</script>

<style lang="scss">
@import '../assets/scss/_variables';

.overlay{
  width: 100%;
  height: 100vh;
  position: fixed;
  display: flex;
  flex-direction: column;
  justify-content: center;
  top: 0;
  left: 0;
  background-color: rgba(34, 34, 34, .6);
  backdrop-filter: blur(2px);
  padding: 10px;

  .card{
    border: 2px solid $color_main;
    width: 100%;

    &__header{
      padding: 20px;
      display: flex;
      border-bottom: 2px solid $color_main;
      position: relative;

      h2{
        color: $color_text;
        text-align: center;
        width: 100%;
        margin-right: -22px;
        color: $color_main;
      }
    }

    &__body{
      padding: 20px;
    }

    &__footer{
      padding: 13px;
      border-top: 2px solid $color_main;

      h3{
        text-align: center;
      }
    }

    &__close-btn{
      background: transparent;
      border: none;
      color: $color_main;
      font-size: 45px;
      position: absolute;
      right: 0;
      top: 0;
      border-left: 2px solid $color_main;
      display: block;
      width:65px;
      height: 65px;
      padding-bottom: 5px;
    }

    &--error{
      border-color: $color_error;

      .card__header, .card__close-btn, .card__footer{
        border-color: $color_error;
      }

      h2, h3, .card__close-btn{
        color: $color_error;
      }
    }

    &--success{
      border-color: $color_success;

      .card__header, .card__close-btn, .card__footer{
        border-color: $color_success;
      }

      h2, h3, .card__close-btn{
        color: $color_success;
      }
    }
  }
}
</style>
