<script lang="ts">
  import { _ } from "svelte-i18n"

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

<div class="bg-gray-50 dark:bg-gray-700">
  <div class="container mx-auto pt-4 lg:pt-8">
    <h1 class="heading1">
      {$_("Case statistics")}
    </h1>

    <nav>
      <ul class="flex flex-col lg:flex-row">
        {#each tabs as tab (tab.id)}
          {@const pathname = `/management/case_statistics/${tab.id}/`}
          {@const isActive = data.url.pathname === pathname}

          <li>
            <a
              class="inline-block p-2 font-bold text-gray-900 hover:bg-white hover:text-orange dark:text-white dark:hover:bg-gray-900"
              class:bg-white={isActive}
              class:dark:bg-gray-900={isActive}
              class:text-orange={isActive}
              href={pathname}
            >
              {tab.name}
            </a>
          </li>
        {/each}
      </ul>
    </nav>
  </div>
</div>

<div class="container mx-auto my-4 lg:my-8">
  <div class="my-4 lg:my-8">
    {#if activeTab}
      <h2 id={activeTab.id} class="heading2">
        {activeTab.name}
      </h2>

      <slot />
    {/if}
  </div>
</div>
