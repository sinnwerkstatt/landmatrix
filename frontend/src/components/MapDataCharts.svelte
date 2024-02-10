<script lang="ts">
  import type { ComponentType } from "svelte"
  import { _ } from "svelte-i18n"

  import ChartsIcon from "$components/Data/Charts/CakeTeaser.svelte"
  import MapIcon from "$components/Data/MapTeaser.svelte"
  import DataIcon from "$components/Data/TableTeaser.svelte"

  // import DataIcon from "./icons/DataIcon.svelte"
  // import MapIcon from "./icons/MapIcon.svelte"
  // import ChartsIcon from "./icons/ChartsIcon.svelte"

  interface Card {
    title: string
    href: string
    description: string
    icon: ComponentType
  }

  const cards: Card[] = [
    {
      title: $_("Map"),
      href: "/map",
      description: $_(
        "Explore the map for information about land deals from global down to regional and country level.",
      ),
      icon: MapIcon,
    },
    {
      title: $_("Data"),
      href: "/list/deals",
      description: $_(
        "Search and filter the dataset through pre-configured entry points or drill down to single deals.",
      ),
      icon: DataIcon,
    },
    {
      title: $_("Charts"),
      href: "/charts",
      description: $_(
        "Generate your own infographics using a wide selection of charts to illustrate information about deals.",
      ),
      icon: ChartsIcon,
    },
  ]
</script>

<div class="my-8 grid grid-cols-1 gap-8 sm:grid-cols-3">
  {#each cards as card}
    <a
      href={card.href}
      class="block rounded bg-gray-50 p-4 text-center text-black hover:text-inherit hover:shadow-[1px_1px_4px_4px] hover:shadow-black/30 dark:bg-gray-700 dark:text-white dark:hover:shadow-white/40"
      on:click
    >
      <h3 class="heading4">{card.title}</h3>
      <svelte:component this={card.icon} class="mx-auto mt-2 text-orange" />
      <div class="body1 mt-6">
        {card.description}
      </div>
    </a>
  {/each}
</div>
