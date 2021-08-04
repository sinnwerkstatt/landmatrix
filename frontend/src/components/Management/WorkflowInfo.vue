<template>
  <div class="comment">
    <div class="meta">
      <span class="date">{{ info.timestamp | dayjs("YYYY-MM-DD HH:mm") }}</span>
      <span class="from-to">
        {{ $t("From") }} {{ info.from_user.username }}
        <span v-if="info.to_user"> {{ $t("to") }} {{ info.to_user.username }} </span>
      </span>
    </div>

    <div
      v-if="info.draft_status_before !== info.draft_status_after"
      class="status-change"
    >
      <template v-if="info.draft_status_before">
        <div class="status">{{ draft_status_map[info.draft_status_before] }}</div>
        →
      </template>
      <div class="status">
        {{ draft_status_map[info.draft_status_after] || status_map[2] }}
      </div>
    </div>

    <div v-if="info.comment" class="message" v-html="linebreaks(info.comment)"></div>
  </div>
</template>

<script>
  import { draft_status_map, status_map } from "$utils/choices";
  import { linebreaks } from "$utils/filters";

  export default {
    name: "ManageHeaderWorkflowInfo",
    props: {
      info: { type: Object, required: true },
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
