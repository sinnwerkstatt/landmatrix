<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { BlogPage } from "$lib/types/wagtail"

  interface Props {
    articles?: BlogPage[]
  }

  let { articles = [] }: Props = $props()
  let limit = $state(3)

  let limitedArticles = $derived(limit ? articles.slice(0, limit) : articles)
</script>

{#each limitedArticles as article}
  <div class="my-2 flex flex-col gap-4 overflow-hidden border-b py-2 sm:flex-row">
    {#if article.header_image}
      <img
        src={article.header_image}
        alt="Header for {article.title}"
        class="aspect-square h-48 w-48"
        loading="lazy"
      />
    {/if}

    <div>
      <h5 class="heading5">
        <a href={article.url} class="text-orange transition hover:text-orange-700">
          {article.title}
        </a>
      </h5>
      {@html article.excerpt}
    </div>
  </div>
{/each}

{#if limit && limit < articles.length}
  <button type="button" class="btn btn-primary" onclick={() => (limit = 0)}>
    {$_("Show all")}
    {articles.length}
  </button>
{/if}
