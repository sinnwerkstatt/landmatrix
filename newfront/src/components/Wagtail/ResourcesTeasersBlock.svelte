<script lang="ts">
  import type { BlogPage } from "$lib/types/wagtail";
  import ArticleList from "$components/Wagtail/ArticleList.svelte";

  export let value: { articles: BlogPage[] };
</script>

<ArticleList articles={value.articles} />
