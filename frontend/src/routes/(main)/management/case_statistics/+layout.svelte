<script lang="ts">
  import { _ } from "svelte-i18n"

  import FilterBar from "./FilterBar.svelte"

  export let data

  let tabs: { id: string; name: string; showFilter: boolean }[]
  $: tabs = [
    {
      id: "deal-quality-indicators",
      name: $_("Deal quality indicators"),
      showFilter: true,
    },
    {
      id: "investor-quality-indicators",
      name: $_("Investor quality indicators"),
      showFilter: false,
    },
    {
      id: "quality-indicators-records",
      name: $_("Quality indicators records"),
      showFilter: false,
    },
    {
      id: "activation-status",
      name: $_("Activation status"),
      showFilter: true,
    },
    {
      id: "changes-over-time",
      name: $_("Changes over time"),
      showFilter: true,
    },
  ]

  $: activeTab = tabs.find(
    x => data.url.pathname === `/management/case_statistics/${x.id}/`,
  )
</script>

<svelte:head>
  <title>{$_("Case statistics")} | {$_("Land Matrix")}</title>
</svelte:head>

<div class="container mx-auto my-4 lg:my-8">
  <h1 class="heading2">
    {$_("Case statistics")}
  </h1>

  <nav>
    <ul class="flex flex-col gap-x-2 border-y border-gray-50 lg:flex-row">
      {#each tabs as tab (tab.id)}
        {@const pathname = `/management/case_statistics/${tab.id}/`}

        <li>
          <a
            class="inline-block p-2"
            class:font-bold={data.url.pathname === pathname}
            href={pathname}
          >
            {tab.name}
          </a>
        </li>
      {/each}
    </ul>
  </nav>

  {#if activeTab && activeTab.showFilter}
    <FilterBar />
  {/if}

  <div class="my-4 lg:my-8">
    {#if activeTab}
      <h2 id={activeTab.id} class="heading3">
        {activeTab.name}
      </h2>
      <slot />
    {/if}
  </div>
</div>
