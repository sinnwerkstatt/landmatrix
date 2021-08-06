<template>
  <div class="comments">
    <h3>Comments</h3>
    <div class="new-comment">
      <form action="." method="post">
        <div>
          <textarea
            ref="comment"
            v-model="comment"
            rows="2"
            required="required"
          ></textarea>
        </div>
        <div class="send">
          <span>{{ $t("Send to:") }}</span>
          <multiselect
            v-model="send_to_user"
            :options="users"
            :multiple="false"
            :close-on-select="true"
            :allow-empty="true"
            placeholder="Send to"
            track-by="id"
            :custom-label="(u) => `${u.full_name} (${u.username})`"
          />
          <a class="btn btn-default" @click.prevent="add_comment">
            {{ $t("Send") }}
          </a>
        </div>
      </form>
    </div>
    <ManageHeaderCommentsList :workflowinfos="object.workflowinfos" />
  </div>
</template>

<script>
  import ManageHeaderCommentsList from "$components/Management/ManageHeaderCommentsList";

  export default {
    name: "ManageHeaderComments",
    components: { ManageHeaderCommentsList },
    props: {
      object: { type: Object, required: true },
      objectVersion: { type: [Number, String], default: null },
      users: { type: Array, required: true },
    },
    data() {
      return {
        comment: "",
        send_to_user: null,
      };
    },

    methods: {
      add_comment() {
        if (!this.$refs.comment.checkValidity()) this.$refs.comment.reportValidity();
        else {
          this.$emit("add_comment", {
            comment: this.comment,
            send_to_user: this.send_to_user,
          });
          this.comment = "";
        }
      },
    },
  };
</script>

<style lang="scss" scoped>
  .comments {
    background: #c4c4c4;
    padding: 0.7rem;
    color: rgba(black, 0.6);
    max-height: 100%;
    flex-grow: 1;
    display: flex;
    flex-direction: column;

    h3 {
      margin-top: 0;
      font-weight: 600;
      margin-bottom: 0.2em;
      font-size: 1.2em;
    }

    .new-comment {
      font-size: 0.9em;
      margin-bottom: 1em;

      textarea {
        padding: 0.2em 0.5em;
        width: 100%;
        border: 1px solid lightgrey;
        border-radius: 5px;
        z-index: 1;
        position: relative;
        font-size: 0.9em;

        &:focus {
          border-color: transparent;
          outline: none;
        }
      }

      .send {
        display: flex;
        align-items: center;

        span {
          white-space: nowrap;
          padding-right: 5px;
        }

        input {
          flex: 1;
          width: 100px;
          margin: 0 2px 0 0.5em;
          border: 1px solid lightgrey;
          border-radius: 5px;
        }

        .btn {
          margin-left: 7px;
          background: var(--color-lm-investor);
          padding: 0.38em 0.7em;
          font-size: 0.9em;
          border-radius: 5px;

          &:hover {
            background-color: var(--color-lm-investor-light);
          }

          &:focus,
          &:active {
            outline: none;
          }
        }
      }
    }
  }
</style>

<style lang="scss">
  .comment .message p:last-child {
    margin-bottom: 0;
  }

  .send {
    .multiselect,
    .multiselect__tags {
      min-height: 30px;
    }

    .multiselect {
      min-width: auto;
    }

    .multiselect__tags {
      padding-top: 4px;
      padding-left: 2px;
      padding-right: 25px;
    }

    .multiselect__select {
      height: 32px;
      width: 32px;
      padding-left: 0;
      padding-right: 0;
    }

    .multiselect__placeholder,
    .multiselect__single {
      margin-bottom: 0 !important;
    }

    .multiselect__placeholder {
      padding-top: 0;
      padding-left: 5px;
    }

    .multiselect__input {
      font-size: 1em;
      margin-bottom: 2px;
    }
  }
</style>
