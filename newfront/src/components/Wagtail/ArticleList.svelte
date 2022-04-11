<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { BlogPage } from "$lib/types/wagtail";

  export let articles: BlogPage[] = [];
  export let articlesLabel: string;
  let limit = 3;

  $: limitedArticles = limit ? articles.slice(0, limit) : articles;
</script>

{#if articles.length > 0}
  <div class=" my-8 m-auto w-[clamp(20rem, 75%, 56rem)]">
    <h3>{$_(articlesLabel)}</h3>
    <slot />
    {#each limitedArticles as article}
      <div class="h-auto row">
        <div class="col-3">
          {#if article.header_image}
            <img
              src={article.header_image}
              alt="Header image for {article.title}"
              class="mb-4"
            />
          {/if}
        </div>
        <div class="col-9">
          <h5 class="title font-bold text-lg">
            <a href={article.url} class="text-orange-500">{article.title}</a>
          </h5>
          <div class="excerpt">
            {@html article.excerpt}
          </div>
        </div>
      </div>
    {/each}
    {#if limit && limit < articles.length}
      <button type="button" class="btn-white" on:click={() => (limit = 0)}>
        {$_("Show all")}
        {articles.length}
        {articlesLabel.toLowerCase()}
      </button>
    {/if}
  </div>
{/if}
