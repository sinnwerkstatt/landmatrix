<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { BlogPage } from "$lib/types/wagtail";

  export let articles: BlogPage[] = [];
  export let articlesLabel: string;
  let limit = 3;

  $: limitedArticles = limit ? articles.slice(0, limit) : articles;
</script>

{#if articles.length > 0}
  <div class=" my-8 m-auto ">
    <h3>{$_(articlesLabel)}</h3>
    <slot />
    {#each limitedArticles as article}
      <div class="h-auto flex flex-row">
        {#if article.header_image}
          <img
            src={article.header_image}
            alt="Header image for {article.title}"
            class="mb-4 w-56 h-56 mr-8"
          />
        {/if}

        <div class="col-9">
          <h5 class="title font-bold text-lg">
            <a href={article.url} class="text-orange">{article.title}</a>
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
