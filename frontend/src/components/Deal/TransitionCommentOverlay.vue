<template>
  <div v-if="show" class="overlay-bg" @click.self="$emit('cancel_transition')">
    <div class="overlay">
      <h3>{{ transition.title }}</h3>
      <!-- no reason, but keep if they redecide
      <div v-if="is_set_confidential" class="reason">
        {{ $t("Reason") }}
        <select ref="reason" v-model="confidential_reason" required="required">
          <option
            v-for="key in Object.keys(confidential_reason_choices)"
            :key="key"
            :value="key"
          >
            {{ $t(confidential_reason_choices[key]) }}
          </option>
        </select>
      </div>-->
      <p>{{ $t("Please provide a comment explaining your request") }}</p>
      <textarea ref="comment" v-model="comment" required="required"></textarea>
      <div class="actions">
        <a class="btn btn-primary" @click.prevent.stop="submit_comment">{{
          transition.title
        }}</a>
        <a class="btn btn-secondary" @click.prevent.stop="$emit('cancel_transition')">{{
          $t("Cancel")
        }}</a>
      </div>
    </div>
  </div>
</template>

<script>
  import { linebreaks } from "$utils/filters";
  import { confidential_reason_choices } from "$utils/choices";

  export default {
    name: "RequiredMessageOverlay",
    props: {
      show: { type: Boolean, default: false },
      transition: null,
    },
    data() {
      return {
        comment: "",
        send_to_user: null,
        confidential_reason: null,
        linebreaks,
      };
    },
    computed: {
      is_set_confidential() {
        return this.transition.transition === "SET_CONFIDENTIAL";
      },
      confidential_reason_choices() {
        return confidential_reason_choices;
      },
    },
    methods: {
      submit_comment() {
        if (this.is_set_confidential) {
          // if (this.$refs.comment.checkValidity() && this.$refs.reason.checkValidity()) {
          if (this.$refs.comment.checkValidity()) {
            this.$emit("do_set_confidential", {
              comment: this.comment,
              reason: this.confidential_reason,
            });
          } else {
            this.$refs.comment.reportValidity();
            //this.$refs.reason.reportValidity();
            return;
          }
        } else {
          // status change
          if (this.$refs.comment.checkValidity()) {
            this.$emit("do_transition", this.comment);
          } else {
            this.$refs.comment.reportValidity();
            return;
          }
        }
        this.comment = "";
        this.reason = null;
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../../scss/colors";
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

    .reason {
      margin-bottom: 1em;

      select {
        background-color: white;
        border-radius: 5px;
        border: 1px solid $lm_grey;
      }
    }

    textarea {
      width: 100%;
      border: 1px solid $lm_grey;
      border-radius: 5px;
      padding: 0.2em 0.5em;

      &:focus {
        border: 1px solid $lm_grey;
        outline: none;
      }
    }

    .actions {
      margin-top: 1em;
      text-align: right;

      .btn {
        margin-left: 0.5em;
      }
    }
  }
</style>
