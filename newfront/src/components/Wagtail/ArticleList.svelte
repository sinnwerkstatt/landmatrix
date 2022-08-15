<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { BlogPage } from "$lib/types/wagtail";

  export let articles: BlogPage[] = [];
  let limit = 3;

  $: limitedArticles = limit ? articles.slice(0, limit) : articles;
</script>

{#each limitedArticles as article}
  <div class="flex flex-col sm:flex-row gap-4 overflow-hidden py-2 my-2 border-b">
    {#if article.header_image}
      <img
        src={article.header_image}
        alt="Header for {article.title}"
        class="w-48 h-48"
      />
    {/if}

    <div>
      <h5 class="font-bold text-lg">
        <a href={article.url} class="text-orange">{article.title}</a>
      </h5>
      {@html article.excerpt}
    </div>
  </div>
{/each}
{#if limit && limit < articles.length}
  <button type="button" class="btn-white" on:click={() => (limit = 0)}>
    {$_("Show all")}
    {articles.length}
  </button>
{/if}
