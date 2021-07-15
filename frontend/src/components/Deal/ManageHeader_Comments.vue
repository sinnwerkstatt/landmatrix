<template>
  <div class="col-md-4 comments">
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
    <div class="comments-list">
      <div v-for="wfi in object.workflowinfos" :key="wfi.timestamp" class="comment">
        <div class="meta">
          <span class="date">{{ wfi.timestamp | dayjs("YYYY-MM-DD HH:mm") }}</span>
          <span class="from-to">
            {{ $t("From") }} {{ wfi.from_user.full_name }}
            <span v-if="wfi.to_user"> {{ $t("to") }} {{ wfi.to_user.full_name }} </span>
          </span>
        </div>

        <div
          v-if="get_draft_status(wfi)"
          class="status-change"
          v-html="get_draft_status(wfi)"
        />

        <div v-if="wfi.comment" class="message" v-html="linebreaks(wfi.comment)"></div>
      </div>
    </div>
  </div>
</template>

<script>
  import { draft_status_map, status_map } from "$utils/choices";
  import { linebreaks } from "$utils/filters";

  export default {
    name: "ManageHeaderComments",
    props: {
      object: { type: Object, required: true },
      objectVersion: { type: [Number, String], default: null },
      users: { type: Array, required: true },
    },
    data() {
      return {
        comment: "",
        send_to_user: null,
        linebreaks,
      };
    },

    methods: {
      get_draft_status(wfi) {
        let before = wfi.draft_status_before;
        let after = wfi.draft_status_after;
        if (before !== after) {
          if (!before) {
            return `<div class="status">${draft_status_map[after]}</div>`;
          } else {
            let before_status = draft_status_map[before];
            let after_status;
            if (!after) {
              after_status = status_map[2];
            } else {
              after_status = draft_status_map[after];
            }
            let ret = `<div class="status">${before_status}</div>`;
            ret += `→`;
            ret += `<div class="status">${after_status}</div>`;
            return ret;
          }
        } else {
          return null;
        }
      },
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
  @import "../../scss/colors";

  .comments {
    background: #c4c4c4;
    padding: 0.7rem;
    color: rgba(black, 0.6);
    max-height: 100%;
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
          background: $lm_investor;
          padding: 0.38em 0.7em;
          font-size: 0.9em;
          border-radius: 5px;

          &:hover {
            background-color: lighten($lm_investor, 5%);
          }

          &:focus,
          &:active {
            outline: none;
          }
        }
      }
    }

    .comments-list {
      margin-top: 1em;
      overflow-y: scroll;
      margin-right: -0.7rem;
      height: 100%;
      box-shadow: inset 0 3px 7px -3px rgba(0, 0, 0, 0.1),
        inset 0px -2px 5px -2px rgba(0, 0, 0, 0.1);
      padding: 2px 4px;
      margin-left: -4px;
      max-height: 330px;

      .comment {
        font-size: 0.8em;
        margin-bottom: 0.5em;

        .meta {
          .date {
            font-weight: 600;
          }
        }

        //.status-change {
        //  margin-bottom: 2px;
        //}

        .message {
          background: #e5e5e5;
          padding: 0.3em 0.5em;
          border-radius: 5px;
        }
      }
    }
  }
</style>

<style lang="scss">
  .status-change .status {
    display: inline-block;
    padding: 2px 5px 3px;
    line-height: 1;
    background-color: darken(#e4e4e4, 8%);
    color: #5e5e64;
    border-radius: 8px;
    filter: drop-shadow(-1px 1px 1px rgba(0, 0, 0, 0.1));

    &:last-child {
      background-color: #93c7c8;
      color: white;
    }
  }
</style>
