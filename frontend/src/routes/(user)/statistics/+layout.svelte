<script lang="ts" context="module">
  export interface Section {
    id: string
    name: string
    tabs: { id: string; name: string }[]
  }
</script>

<script lang="ts">
  import { _ } from "svelte-i18n"

  export let data

  let sections: Section[]
  $: sections = [
    {
      id: "quality",
      name: $_("Quality"),
      tabs: [
        {
          id: "deal",
          name: $_("Deal"),
        },
        {
          id: "investor",
          name: $_("Investor"),
        },
        {
          id: "over-time",
          name: $_("Over time"),
        },
      ],
    },
    {
      id: "quantity",
      name: $_("Quantity"),
      tabs: [
        {
          id: "by-status",
          name: $_("By status"),
        },
        {
          id: "over-time",
          name: $_("Over time"),
        },
      ],
    },
  ]
</script>

<svelte:head>
  <title>{$_("Statistics")} | {$_("Land Matrix")}</title>
</svelte:head>

<div class="bg-gray-50 dark:bg-gray-700">
  <div class="container mx-auto pt-4 lg:pt-8">
    <h1 class="heading1">
      {$_("Statistics")}
    </h1>

    <nav class="flex gap-8">
      {#each sections as section (section.id)}
        <div class="flex items-baseline">
          <div class="px-2 font-bold after:content-[':']">
            {section.name}
          </div>

          <ul class="flex flex-col lg:flex-row">
            {#each section.tabs as tab (tab.id)}
              {@const url = new URL(`../../${section.id}/${tab.id}/`, data.url)}
              {@const isActive = data.url.pathname === url.pathname}

              <li>
                <a
                  class="inline-block p-2 font-bold text-gray-900 hover:bg-white hover:text-orange dark:text-white dark:hover:bg-gray-900"
                  class:is-active={isActive}
                  href={url.pathname}
                >
                  {tab.name}
                </a>
              </li>
            {/each}
          </ul>
        </div>
      {/each}
    </nav>
  </div>
</div>

<div class="container mx-auto my-4 lg:my-8">
  <div class="my-4 lg:my-8">
    <slot />
  </div>
</div>

<style lang="postcss">
  .is-active {
    @apply bg-white text-orange dark:bg-gray-900;
  }
</style>
