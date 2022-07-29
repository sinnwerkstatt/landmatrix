<script lang="ts">
  import type { BlogPage } from "$lib/types/wagtail";
  import ArticleList from "$components/Wagtail/ArticleList.svelte";

  export let value: { articles: BlogPage[] };
</script>

<div data-block="resources_teasers">
  <ArticleList articles={value.articles} />
</div>
