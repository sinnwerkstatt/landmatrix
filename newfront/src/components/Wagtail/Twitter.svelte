<script lang="ts">
  import dayjs from "dayjs"

  import type { TwitterFeed } from "$lib/types/wagtail"

  export let twitterFeed: TwitterFeed

  $: timeline = twitterFeed?.timeline || []
</script>

<div class="twitter-timeline">
  {#each timeline as status}
    <div class="my-3">
      <div>
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
        <a target="_blank" href={status.deep_link}>
          {dayjs(status.created_at).format("YYYY-MM-DD HH:mm")}
        </a>
      </div>
      <div>{@html status.text}</div>
    </div>
  {/each}
  {#if timeline.length === 0}
    <div>Feed currently not available.</div>
  {/if}

  <a
    href="https://twitter.com/{twitterFeed.username}"
    target="_blank"
    class="btn border-orange font-bold"
  >
    Tweets by {twitterFeed.username}
  </a>
</div>
