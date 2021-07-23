<template>
  <div class="overlay-bg" @click.self="$emit('cancel')">
    <div class="overlay">
      <h3 v-if="title">{{ title }}</h3>
      <form @submit.stop.prevent="submit">
        <slot></slot>

        <template v-if="commentInput">
          <label>{{ $t("Please provide a comment explaining your request") }}</label>
          <textarea
            ref="comment"
            v-model="comment"
            :required="commentRequired"
          ></textarea>
        </template>
        <div class="actions">
          <button type="submit" class="btn btn-primary">
            {{ title || $t("Submit") }}
          </button>
          <button class="btn btn-secondary" @click.stop="$emit('cancel')">
            {{ $t("Cancel") }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Overlay",
    props: {
      title: { type: String, default: "" },
      commentInput: { type: Boolean, default: false },
      commentRequired: { type: Boolean, default: false },
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
      submit(e) {
        if (e.target.checkValidity()) {
          this.$emit("submit", { comment: this.comment });
        } else {
          e.target.reportValidity();
        }
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "node_modules/bootstrap/scss/functions";
  @import "node_modules/bootstrap/scss/variables";
  @import "node_modules/bootstrap/scss/mixins/_breakpoints";

  textarea {
    width: 100%;
    border: 1px solid var(--color-lm-light);
    border-radius: 5px;
    padding: 0.2em 0.5em;

    &:focus {
      border: 1px solid var(--color-lm-light);
      outline: none;
    }
  }

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
    color: var(--color-lm-dark);
    border-color: var(--color-lm-orange);
    background-color: var(--color-lm-light);

    .actions {
      margin-top: 1em;
      text-align: right;

      .btn {
        margin-left: 0.5em;
      }
    }
  }
</style>
