<template>
  <Overlay
    :title="transition.title"
    @cancel="$emit('cancel_transition')"
    @submit="submit_comment"
  >
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
    <label>{{ $t("Please provide a comment explaining your request") }}</label>
    <textarea ref="comment" v-model="comment" required="required"></textarea>
    <div v-if="toUser" class="assign-to-user">
      <label>{{ $t("Assign to user") }}</label>
      <multiselect
        :value="selected_user"
        :options="users"
        :multiple="false"
        :close-on-select="true"
        :allow-empty="false"
        placeholder="Send to"
        track-by="id"
        label="full_name"
        @select="select_user"
      />
    </div>
  </Overlay>
</template>

<script>
  import Overlay from "$components/Overlay";

  import { confidential_reason_choices } from "$utils/choices";

  export default {
    name: "TransitionCommentOverlay",
    components: { Overlay },
    props: {
      transition: { type: Object, required: true },
      users: {
        type: Array,
        default() {
          return [];
        },
      },
      toUser: { type: Object, default: null },
    },
    data() {
      return {
        comment: "",
        confidential_reason: null,
        to_user_selected: null,
      };
    },
    computed: {
      is_set_confidential() {
        return this.transition && this.transition.key === "SET_CONFIDENTIAL";
      },
      confidential_reason_choices() {
        return confidential_reason_choices;
      },
      selected_user() {
        return this.to_user_selected ? this.to_user_selected : this.toUser;
      },
    },
    methods: {
      select_user(user) {
        this.to_user_selected = user;
      },
      submit_comment() {
        if (this.is_set_confidential) {
          // if (this.$refs.comment.checkValidity() && this.$refs.reason.checkValidity()) {
          if (this.$refs.comment.checkValidity()) {
            this.$emit("do_set_confidential", {
              force: true,
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
            console.log(this.selected_user);
            this.$emit("do_transition", {
              comment: this.comment,
              to_user: this.selected_user,
            });
          } else {
            this.$refs.comment.reportValidity();
            return;
          }
        }
        this.comment = "";
        this.reason = null;
        this.to_user_selected = null;
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../../scss/colors";
  @import "node_modules/bootstrap/scss/functions";
  @import "node_modules/bootstrap/scss/variables";
  @import "node_modules/bootstrap/scss/mixins/_breakpoints";

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

  .assign-to-user {
    margin-top: 1em;

    .multiselect {
      border: 1px solid $lm_grey;
      border-radius: 5px;
    }
  }
</style>
