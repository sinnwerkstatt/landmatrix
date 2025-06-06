<script lang="ts" module>
  export interface Section {
    id: string
    name: string
    tabs: { id: string; name: string }[]
  }
</script>

<script lang="ts">
  import { _ } from "svelte-i18n"

  import { afterNavigate } from "$app/navigation"

  let { data, children } = $props()

  let lastFocusedElement: HTMLAnchorElement | null = null

  const handleFocus = (event: FocusEvent) => {
    lastFocusedElement = event.target as HTMLAnchorElement | null
  }

  afterNavigate(() => {
    if (lastFocusedElement) lastFocusedElement.focus()
  })

  let sections: Section[] = $derived([
    {
      id: "quality",
      name: $_("Data quality"),
      tabs: [
        {
          id: "deal",
          name: $_("Deals"),
        },
        {
          id: "investor",
          name: $_("Investors"),
        },
        {
          id: "over-time",
          name: $_("Over time"),
        },
      ],
    },
    {
      id: "quantity",
      name: $_("Data quantity"),
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
  ])
</script>

<svelte:head>
  <title>{$_("Data Statistics")} | {$_("Land Matrix")}</title>
</svelte:head>

<div class="bg-gray-50 dark:bg-gray-700">
  <div class="container mx-auto pt-4 lg:pt-8">
    <h1 class="heading1">
      {$_("Data Statistics")}
    </h1>

    <nav class="flex gap-8">
      {#each sections as section (section.id)}
        <div class="flex items-baseline">
          <div class="px-4 font-bold underline after:content-[':']">
            {section.name}
          </div>

          <ul class="flex flex-col lg:flex-row">
            {#each section.tabs as tab (tab.id)}
              {@const url = new URL(`../../${section.id}/${tab.id}/`, data.url)}
              {@const isActive = data.url.pathname === url.pathname}

              <li>
                <!-- TODO: Use custom components -->
                <a
                  class="
                    inline-block px-4 py-2 font-bold text-gray-900
                    hover:bg-white hover:text-orange
                    focus:relative focus:z-10
                    dark:text-white dark:hover:bg-gray-900
                  "
                  class:is-active={isActive}
                  onfocus={handleFocus}
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
    {@render children?.()}
  </div>
</div>

<style lang="postcss">
  .is-active {
    @apply bg-white text-orange;

    :global {
      @apply dark:bg-gray-900;
    }
  }
</style>
