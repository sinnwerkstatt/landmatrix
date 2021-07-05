<template>
  <div class="overlay-bg" @click.self="$emit('cancel')">
    <div class="overlay">
      <h3 v-if="title">{{ title }}</h3>
      <slot></slot>

      <div class="actions">
        <a class="btn btn-primary" @click.stop="submit">{{ title || $t("Submit") }}</a>
        <a class="btn btn-secondary" @click.stop="$emit('cancel')">
          {{ $t("Cancel") }}
        </a>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Overlay",
    props: {
      title: { type: String, default: "" },
    },
    data() {
      return {
        comment: "",
        confidential_reason: null,
        to_user_selected: null,
      };
    },
    created() {
      document.addEventListener("keydown", this.cancel);
    },
    beforeDestroy() {
      document.removeEventListener("keydown", this.cancel);
    },
    methods: {
      cancel(e) {
        if (e.key === "Escape") this.$emit("cancel");
      },
      submit() {
        this.$emit("submit");
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../scss/colors";
  @import "node_modules/bootstrap/scss/functions";
  @import "node_modules/bootstrap/scss/variables";
  @import "node_modules/bootstrap/scss/mixins/_breakpoints";

  .overlay-bg {
    position: fixed;
    top: 0;
    width: 100vw;
    height: 100vh;
    z-index: 2000;
    background-color: rgba(black, 0.3);
    backdrop-filter: blur(3px);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .overlay {
    width: 70vw;
    max-width: 800px;
    min-width: 300px;

    @include media-breakpoint-down(sm) {
      width: 85vw;
    }

    padding: 0.8em 1.8em 1.8em;
    box-shadow: 0 0 15px rgba(black, 0.5);
    color: $lm_dark;
    border-color: $lm_orange;
    background-color: $lm_light;

    .actions {
      margin-top: 1em;
      text-align: right;

      .btn {
        margin-left: 0.5em;
      }
    }
  }
</style>
