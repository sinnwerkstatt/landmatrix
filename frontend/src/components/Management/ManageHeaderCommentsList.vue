<template>
  <div class="comments-list">
    <div v-for="wfi in workflowinfos" :key="wfi.timestamp" class="comment">
      <div class="meta">
        <span class="date">{{ wfi.timestamp | dayjs("YYYY-MM-DD HH:mm") }}</span>
        <span class="from-to">
          {{ $t("From") }} {{ wfi.from_user.username }}
          <span v-if="wfi.to_user"> {{ $t("to") }} {{ wfi.to_user.username }} </span>
        </span>
      </div>

      <div
        v-if="wfi.draft_status_before !== wfi.draft_status_after"
        class="status-change"
      >
        <template v-if="wfi.draft_status_before">
          <div class="status">{{ draft_status_map[wfi.draft_status_before] }}</div>
          →
        </template>
        <div class="status">
          {{ draft_status_map[wfi.draft_status_after] || status_map[2] }}
        </div>
      </div>

      <div v-if="wfi.comment" class="message" v-html="linebreaks(wfi.comment)"></div>
    </div>
  </div>
</template>

<script>
  import { draft_status_map, status_map } from "$utils/choices";
  import { linebreaks } from "$utils/filters";

  export default {
    name: "ManageHeaderCommentsList",
    props: {
      workflowinfos: { type: Array, required: true },
    },
    data() {
      return {
        draft_status_map,
        status_map,
        linebreaks,
      };
    },
    methods: {},
  };
</script>

<style scoped lang="scss">
  .comments-list {
    cursor: default;
    background: #c4c4c4;
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
