<script lang="ts">
  import dayjs from "dayjs"

  import type { TwitterFeed } from "$lib/types/wagtail"

  interface Props {
    twitterFeed: TwitterFeed
  }

  let { twitterFeed }: Props = $props()

  let timeline = $derived(twitterFeed?.timeline || [])
</script>

<div class="twitter-timeline">
  {#each timeline as status}
    <div class="my-3">
      <div>
        <a
          href="https://twitter.com/{status.screen_name}"
          target="_blank"
          class="font-bold"
          rel="noreferrer"
        >
          {status.name}
        </a>
        ·
        <a
          href="https://twitter.com/{status.screen_name}"
          target="_blank"
          rel="noreferrer"
          class="twitter-timeline-screenname"
        >
          @{status.screen_name}
        </a>
        ·
        <a target="_blank" rel="noreferrer" href={status.deep_link}>
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
    rel="noreferrer"
    class="btn border-orange font-bold"
  >
    Tweets by {twitterFeed.username}
  </a>
</div>
