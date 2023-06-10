<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { BlogPage } from "$lib/types/wagtail"

  export let articles: BlogPage[] = []
  let limit = 3

  $: limitedArticles = limit ? articles.slice(0, limit) : articles
</script>

{#each limitedArticles as article}
  <div class="my-2 flex flex-col gap-4 overflow-hidden border-b py-2 sm:flex-row">
    {#if article.header_image}
      <img
        src={article.header_image}
        alt="Header for {article.title}"
        class="h-48 w-48"
        loading="lazy"
      />
    {/if}

    <div>
      <h5 class="text-lg font-bold">
        <a href={article.url} class="text-orange">{article.title}</a>
      </h5>
      {@html article.excerpt}
    </div>
  </div>
{/each}
{#if limit && limit < articles.length}
  <button type="button" class="btn btn-white" on:click={() => (limit = 0)}>
    {$_("Show all")}
    {articles.length}
  </button>
{/if}
