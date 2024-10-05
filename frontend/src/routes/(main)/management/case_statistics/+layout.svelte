<script lang="ts">
  import { _ } from "svelte-i18n"

  import FilterBar from "./FilterBar.svelte"

  export let data

  let tabs: { id: string; name: string }[]
  $: tabs = [
    {
      id: "quality-indicators",
      name: $_("Quality indicators"),
    },
    {
      id: "quality-indicators-over-time",
      name: $_("Quality indicators over time"),
    },
    {
      id: "activation-status",
      name: $_("Activation status"),
    },
    {
      id: "changes-over-time",
      name: $_("Changes over time"),
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

  <FilterBar />

  <div class="my-4 lg:my-8">
    {#if activeTab}
      <h2 id={activeTab.id} class="heading3">
        {activeTab.name}
      </h2>
      <slot />
    {/if}
  </div>
</div>
