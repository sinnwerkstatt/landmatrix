<template>
  <div class="widget-twitter-timeline">
    <div
      v-for="status in timeline"
      :key="status.id"
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
        <a target="_blank" :href="status.deep_link" class="twitter-timeline-time">
          {{ dayjs(status.created_at).format("MMM. DD, YYYY, H:mm") }}
        </a>
      </div>
      <div class="twitter-timeline-text" v-html="status.text" />
    </div>
    <div v-if="timeline.length === 0" class="twitter-timeline-empty">
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
    props: {
      value: { type: Object, required: true },
    },
    computed: {
      timeline() {
        return (this.value && this.value.timeline) || [];
      },
    },
    methods: {
      dayjs: dayjs,
    },
  };
</script>

<style lang="scss" scoped>
  .twitter-timeline-username {
    font-weight: bold;
  }

  .tweets-by-btn {
    color: var(--color-lm-orange);
    border-color: var(--color-lm-orange);
    border-width: 2px;
    background: #fcfcfc;
    font-weight: bold;
    /* opacity: 0.5; */
    box-shadow: none;
    text-shadow: none;
  }
</style>
