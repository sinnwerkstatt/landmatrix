<script lang="ts">
  import type { BlogPage } from "$lib/types/wagtail"

  import ArticleList from "$components/Wagtail/ArticleList.svelte"

  interface Props {
    value: { articles: BlogPage[] }
  }

  let { value }: Props = $props()
</script>

<div data-block="resources_teasers">
  <ArticleList articles={value.articles} />
</div>
