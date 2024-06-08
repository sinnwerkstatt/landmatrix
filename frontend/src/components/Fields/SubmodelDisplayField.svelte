<script lang="ts" context="module">
  // https://github.com/dummdidumm/rfcs/blob/ts-typedefs-within-svelte-components/text/ts-typing-props-slots-events.md

  /* eslint-disable @typescript-eslint/no-unused-vars */
  import type { SubmodelEntry } from "$lib/utils/data_processing"

  /* eslint-enable @typescript-eslint/no-unused-vars */
</script>

<script lang="ts" generics="T extends SubmodelEntry">
  import { onMount } from "svelte"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import { isElementInViewport } from "$lib/utils/domHelpers"

  /* eslint-disable no-undef */
  export let entries: T[]
  /* eslint-enable no-undef */

  export let label: string

  let selectedEntryId: string | undefined
  $: selectedEntryId = $page.url.hash?.replace("#", "")

  $: browser && scrollEntryIntoView(selectedEntryId)

  const scrollEntryIntoView = (elemId: string | undefined) => {
    if (!elemId) return

    const el = document.getElementById(elemId ?? "")
    if (el && !isElementInViewport(el)) {
      el.scrollIntoView({ block: "nearest", inline: "nearest" })
    }
  }

  onMount(() => scrollEntryIntoView(selectedEntryId))
</script>

{#if entries.length > 0}
  <section class="w-full">
    {#each entries as entry, index}
      <div
        id={entry.nid}
        class="p-2 {selectedEntryId === entry.nid
          ? 'animate-fadeToWhite dark:animate-fadeToGray'
          : ''}"
      >
        <h3 class="heading4">
          <a href="#{entry.nid}">
            {index + 1}. {label}
            <small class="text-sm text-gray-500">
              #{entry.nid}
            </small>
          </a>
        </h3>
        <slot {entry} />
      </div>
    {/each}
  </section>
{/if}
