<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { BlogPage } from "$lib/types/wagtail"

  interface Props {
    articles?: BlogPage[]
  }

  let { articles = [] }: Props = $props()
</script>

{#each articles as article}
  <div class="mb-12">
    <p class="caption text-orange">{article.categories[0].name}</p>
    <h4 class="heading4 -mt-3 text-orange">{article.title}</h4>

    <div class="body2 -mt-3 mb-6">{article.date}</div>
    <p class="body1 excerpt">
      {@html article.excerpt}
    </p>
    <a class="btn-link btn-secondary p-0" href={article.url}>{$_("Read more")} >></a>
  </div>
{/each}

<style>
  .excerpt {
    overflow: hidden;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
  }
</style>
