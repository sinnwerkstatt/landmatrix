<script lang="ts" context="module">
  // https://github.com/dummdidumm/rfcs/blob/ts-typedefs-within-svelte-components/text/ts-typing-props-slots-events.md

  /* eslint-disable-next-line @typescript-eslint/no-unused-vars */
  import type { Submodel } from "$lib/utils/dataProcessing"
</script>

<script lang="ts" generics="T extends Submodel">
  import { onMount } from "svelte"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import type { SubmodelIdKeys } from "$lib/utils/dataProcessing"
  import { scrollEntryIntoView } from "$lib/utils/domHelpers"

  /* eslint-disable no-undef */
  export let entries: readonly T[]
  /* eslint-enable no-undef */

  export let label: string
  export let selectedEntryId: string | undefined = undefined // for external reference
  export let entryIdKey: SubmodelIdKeys = "nid"

  $: selectedEntryId = $page.url.hash?.replace("#", "") || undefined

  $: browser && scrollEntryIntoView(selectedEntryId)

  onMount(() => scrollEntryIntoView(selectedEntryId))
</script>

{#if entries.length > 0}
  <section class="w-full">
    {#each entries as entry, index (entry[entryIdKey])}
      {@const isSelectedEntry = selectedEntryId === `${entry[entryIdKey]}`}
      <article
        id={`${entry[entryIdKey]}`}
        class="p-2 {isSelectedEntry
          ? 'animate-fadeToWhite dark:animate-fadeToGray'
          : ''}"
      >
        <h3 class="heading4">
          <a href="#{entry[entryIdKey]}">
            {index + 1}. {label}
            <small class="text-sm text-gray-500">
              #{entry[entryIdKey]}
            </small>
          </a>
        </h3>
        <slot {entry} />
      </article>
    {/each}
  </section>
{/if}
