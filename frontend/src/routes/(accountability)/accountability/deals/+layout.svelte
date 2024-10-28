<script lang="ts">
  import { page } from "$app/stores"

  import { fetchDeals } from "$lib/accountability/deals.js"
  import { filters } from "$lib/accountability/filters.js"
  import { deals, dealsHistory } from "$lib/accountability/stores"

  // import Avatar from "$components/Accountability/atomic/Avatar.svelte"
  import DealsMenu from "$components/Accountability/DealsMenu.svelte"
  import FiltersSidebar from "$components/Accountability/FiltersSidebar.svelte"
  import PageHeading from "$components/Accountability/PageHeading.svelte"
  import ProjectModal from "$components/Accountability/ProjectModal.svelte"
  import ProjectsSidebar from "$components/Accountability/ProjectsSidebar.svelte"

  export let data

  // If currentProject =/= page.params.project, update project and empty current page and current Deal
  function updateLocalStorage(pathname) {
    if ($page.params.project) {
      dealsHistory.set(pathname)
    }
  }

  $: updateLocalStorage($page.url.pathname)

  $: fetchDeals($filters)

  $: console.log($deals)
  $: console.log(data)
</script>

<div class="flex h-screen w-full flex-row flex-nowrap bg-a-gray-50">
  <ProjectsSidebar />
  <FiltersSidebar />
  <div class="flex h-screen w-full flex-col px-4">
    <PageHeading />
    <div class="mb-6 flex flex-wrap justify-between gap-6">
      <DealsMenu />
      <span class="text-a-gray-400">Users placeholder</span>
      <!-- <Avatar /> -->
    </div>
    <div class="h-full overflow-auto pb-10">
      <slot />
    </div>
  </div>
</div>

<ProjectModal />
