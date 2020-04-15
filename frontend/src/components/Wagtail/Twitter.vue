<template>
  <div class="widget-twitter-timeline">
    <div
      v-if="value.timeline"
      v-for="status in value.timeline"
      class="twitter-timeline-update my-3"
    >
      <div class="twitter-timeline-meta">
        <a
          :href="`https://twitter.com/${status.screen_name}`"
          target="_blank"
          class="twitter-timeline-username"
        >
          {{ status.name }}
        </a>
        ·
        <a
          :href="`https://twitter.com/${status.screen_name}`"
          target="_blank"
          class="twitter-timeline-screenname"
        >
          @{{ status.screen_name }}
        </a>
        ·
        <a
          target="_blank"
          :href="`https://twitter.com/statuses/${status.id_str}`"
          class="twitter-timeline-time"
        >
          {{ dayjs(status.created_at).format("MMM. DD, YYYY, H:mm") }}
        </a>
      </div>
      <div class="twitter-timeline-text" v-html="status.text" />
    </div>
    <div v-else class="twitter-timeline-empty">
      Feed currently not available.
    </div>

    <a
      :href="`https://twitter.com/${value.username}`"
      target="_blank"
      class="btn tweets-by-btn"
      >Tweets by @{{ value.username }}</a
    >
  </div>
</template>

<script>
  import dayjs from "dayjs";

  export default {
    props: ["value"],
    methods: {
      dayjs: dayjs,
    },
  };
</script>

<style lang="scss">
  .twitter-timeline-username {
    font-weight: bold;
  }

  .tweets-by-btn {
    color: #fc941f;
    border-color: #fc941f;
    border-width: 2px;
    background: #fcfcfc;
    font-weight: bold;
    /* opacity: 0.5; */
    box-shadow: none;
    text-shadow: none;
  }
</style>
