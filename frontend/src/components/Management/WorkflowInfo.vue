<template>
  <div :class="{ unread }" class="comment">
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
    <div v-if="confidential_status_change" class="status-change">
      <div class="status" :class="confidential_status_change">
        {{ $t("Confidential") }}
      </div>
    </div>

    <div v-if="comment_wo_head" class="message">
      {{ comment_wo_head }}
      <button v-if="unread" class="action" @click.prevent="processInfo">
        <i class="fas fa-check-circle fa-lg orange"></i>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
  import { draft_status_map, status_map } from "$utils/choices";
  import Vue, { PropType } from "vue";
  import type { WorkflowInfo } from "$types/generics";
  import gql from "graphql-tag";

  export default Vue.extend({
    name: "WorkflowInfo",
    props: {
      info: { type: Object as PropType<WorkflowInfo>, required: true },
    },
    data() {
      return {
        draft_status_map,
        status_map,
      };
    },
    computed: {
      confidential_status_change(): string | boolean {
        if (this.info.comment?.startsWith("[SET_CONFIDENTIAL]"))
          return "set_confidential";
        if (this.info.comment?.startsWith("[UNSET_CONFIDENTIAL]"))
          return "unset_confidential";
        return false;
      },
      comment_wo_head(): string {
        return this.info.comment
          ?.replace("[SET_CONFIDENTIAL]", "")
          .replace("[UNSET_CONFIDENTIAL] ", "");
      },
      unread(): boolean {
        return (
          this.info.to_user?.username === this.$store.state.page.user.username &&
          !this.info.processed_by_receiver &&
          this.comment_wo_head.length > 0
        );
      },
    },
    methods: {
      async processInfo() {
        let res = await this.$apollo.mutate({
          mutation: gql`
            mutation ($id: Int!, $type: String!) {
              toggle_workflow_info_unread(id: $id, type: $type)
            }
          `,
          variables: { id: this.info.id, type: this.info.__typename },
        });
        if (res.data.toggle_workflow_info_unread)
          // eslint-disable-next-line vue/no-mutating-props
          this.info.processed_by_receiver = true;
      },
    },
  });
</script>

<style scoped lang="scss">
  .comment {
    font-size: 0.8em;
    margin-bottom: 0.5em;

    &.unread {
      font-weight: bold !important;
    }
    .meta {
      .date {
        font-weight: 600;
      }
    }

    .message {
      background: #e5e5e5;
      padding: 0.3em 0.5em;
      border-radius: 5px;
      white-space: pre-line;
      position: relative;
      .action {
        position: absolute;
        top: 0.2rem;
        right: 1rem;
        border: 0;
        background: 0;
        opacity: 0.7;
        transition: opacity 100ms ease;
        &:hover {
          opacity: 1;
        }
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
    &.set_confidential {
      background: red;
    }
    &.unset_confidential {
      background: #5dbe00;
      text-decoration: line-through;
    }
  }
</style>
