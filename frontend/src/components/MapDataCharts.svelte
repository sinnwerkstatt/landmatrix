<script lang="ts">
  import { _ } from "svelte-i18n"
  import cn from "classnames"
  import type { ComponentType } from "svelte"

  import DataIcon from "./icons/DataIcon.svelte"
  import MapIcon from "./icons/MapIcon.svelte"
  import ChartsIcon from "./icons/ChartsIcon.svelte"

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
      class={cn(
        "block bg-lm-lightgray p-4 dark:bg-gray-700",
        "text-center text-black hover:text-inherit dark:text-white",
        "hover:shadow-[1px_1px_4px_4px] hover:shadow-black/30 dark:hover:shadow-white/40",
      )}
      on:click
    >
      <h3>{card.title}</h3>
      <svelte:component this={card.icon} class="mx-auto mt-2 h-20 text-orange" />
      <div class="mt-6 text-lg">
        {card.description}
      </div>
    </a>
  {/each}
</div>
