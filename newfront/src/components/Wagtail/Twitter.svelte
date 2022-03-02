<script>
  import dayjs from "dayjs";
  export let value;

  $: timeline = value?.timeline || [];
</script>

<div class="widget-twitter-timeline">
  {#each timeline as status}
    <div class="twitter-timeline-update my-3">
      <div class="twitter-timeline-meta">
        <a
          href="https://twitter.com/{status.screen_name}"
          target="_blank"
          class="font-bold"
        >
          {status.name}
        </a>
        ·
        <a
          href="https://twitter.com/{status.screen_name}"
          target="_blank"
          class="twitter-timeline-screenname"
        >
          @{status.screen_name}
        </a>
        ·
        <a target="_blank" href={status.deep_link} class="twitter-timeline-time">
          {dayjs(status.created_at).format("MMM. DD, YYYY, H:mm")}
        </a>
      </div>
      <div class="twitter-timeline-text">{@html status.text}</div>
    </div>
  {/each}
  {#if timeline.length === 0}
    <div class="twitter-timeline-empty">Feed currently not available.</div>
  {/if}

  <a
    href="https://twitter.com/{value.username}"
    target="_blank"
    class="btn tweets-by-btn"
  >
    Tweets by @{value.username}
  </a>
</div>

<style>
  .tweets-by-btn {
    /*@apply text-orange;*/
    /*border-color: var(--color-lm-orange);*/
    border-width: 2px;
    background: #fcfcfc;
    font-weight: bold;
    /* opacity: 0.5; */
    box-shadow: none;
    text-shadow: none;
  }
</style>
