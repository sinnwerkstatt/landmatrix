<script lang="ts">
  import { page } from "$app/state"

  function getCurrentTab(path) {
    if (path.includes("scoring")) return "scoring"
    if (path.includes("results")) return "results"
    return "overview"
  }

  function writeHref(project, path) {
    let href = `/accountability/deals/${project}/`
    if (path) href += `${path}/`
    return href
  }

  let currentTab = $derived(getCurrentTab(page.url.pathname))

  let hrefOverview = $derived(writeHref(page.params.project, ""))
  let hrefScoring = $derived(writeHref(page.params.project, "scoring"))
  // $: hrefResults = writeHref($page.params.project, "results")
</script>

<div class="flex">
  <ul class="flex justify-center gap-1">
    <li class={currentTab == "overview" ? "active" : ""}>
      <a href={hrefOverview}>Overview</a>
    </li>
    <li class={currentTab == "scoring" ? "active" : ""}>
      <a href={hrefScoring}>Scoring</a>
    </li>
    <!-- <li class={currentTab == "results" ? "active" : ""}>
      <a href={hrefResults}>Results</a>
    </li> -->
  </ul>
</div>

<style>
  /* Style matches Tabs.svelte */
  a {
    @apply w-fit;
    @apply px-[0.63rem] py-[0.44rem];
    @apply text-a-sm text-a-gray-400;
    @apply rounded-lg border border-a-gray-200;
    @apply bg-white;
  }
  a:hover {
    @apply cursor-pointer;
    @apply bg-a-gray-200 text-a-gray-900;
  }
  li.active > a {
    @apply border-a-gray-900 bg-a-gray-900 text-white;
  }
</style>
