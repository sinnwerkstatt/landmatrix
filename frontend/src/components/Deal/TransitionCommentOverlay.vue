<template>
  <Overlay
    :title="transition.title"
    @cancel="$emit('cancel_transition')"
    @submit="submit_comment"
  >
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
        :custom-label="(u) => `${u.full_name} (${u.username})`"
        @select="select_user"
      />
    </div>
  </Overlay>
</template>

<script>
  import Overlay from "$components/Overlay";

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

        to_user_selected: null,
      };
    },
    computed: {
      selected_user() {
        return this.to_user_selected ? this.to_user_selected : this.toUser;
      },
    },
    methods: {
      select_user(user) {
        this.to_user_selected = user;
      },
      submit_comment() {
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
        this.comment = "";
        this.to_user_selected = null;
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "node_modules/bootstrap/scss/functions";
  @import "node_modules/bootstrap/scss/variables";
  @import "node_modules/bootstrap/scss/mixins/_breakpoints";

  .assign-to-user {
    margin-top: 1em;

    .multiselect {
      border: 1px solid var(--color-lm-light);
      border-radius: 5px;
    }
  }
</style>
