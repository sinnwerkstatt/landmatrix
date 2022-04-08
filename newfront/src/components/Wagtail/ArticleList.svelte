<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { BlogPage } from "$lib/types/wagtail";

  export let articles: BlogPage[] = [];
  export let articlesLabel: string;
  let limit = 3;

  $: limitedArticles = limit ? articles.slice(0, limit) : articles;
</script>

{#if articles.length > 0}
  <div class="articles clamp-20-75p-56">
    <h3>{$_(articlesLabel)}</h3>
    <slot />
    {#each limitedArticles as article}
      <div class="article row">
        <div class="col-3">
          {#if article.header_image}
            <img src={article.header_image} alt="Header image for {article.title}" />
          {/if}
        </div>
        <div class="col-9">
          <h5 class="title">
            <a href={article.url}>{article.title}</a>
          </h5>
          <div class="excerpt">
            {@html article.excerpt}
          </div>
        </div>
      </div>
    {/each}
    {#if limit && limit < articles.length}
      <button type="button" on:click={() => (limit = 0)}>
        {$_("Show all")}
        {articles.length}
        {articlesLabel.toLowerCase()}
      </button>
    {/if}
  </div>
{/if}

<!--TODO Charlotte-->
<!--<style lang="scss" scoped>-->
<!--  .articles {-->
<!--    margin-top: 2em;-->
<!--    margin-bottom: 2em;-->
<!--    h4 {-->
<!--      font-size: 18px;-->
<!--      margin-bottom: 1.2em;-->
<!--    }-->
<!--    h5 {-->
<!--      font-size: 18px;-->
<!--      a {-->
color: var(--color-lm-orange);
<!--      }-->
<!--    }-->
<!--    img {-->
<!--      max-width: 100%;-->
<!--    }-->
<!--    .article {-->
<!--      img {-->
<!--        height: auto;-->
<!--      }-->
<!--      margin-bottom: 1em;-->
<!--    }-->
<!--    button {-->
<!--      border: 1px solid black;-->
<!--      padding: 0.2em 1.2em;-->
<!--      font-size: 14px;-->
<!--      text-transform: uppercase;-->
<!--      color: black;-->
<!--    }-->
<!--  }-->
<!--</style>-->
