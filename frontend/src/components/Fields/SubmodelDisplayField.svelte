<script lang="ts" context="module">
  // https://github.com/dummdidumm/rfcs/blob/ts-typedefs-within-svelte-components/text/ts-typing-props-slots-events.md

  /* eslint-disable-next-line @typescript-eslint/no-unused-vars */
  import type { Submodel } from "$lib/utils/dataProcessing"
</script>

<script lang="ts" generics="T extends Submodel">
  import { onMount } from "svelte"

  import { browser } from "$app/environment"
  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  import type { SubmodelIdKeys } from "$lib/utils/dataProcessing"
  import { scrollEntryIntoView } from "$lib/utils/domHelpers"

  /* eslint-disable no-undef */
  export let entries: readonly T[]
  /* eslint-enable no-undef */

  export let label: string
  export let selectedEntryId: string | undefined = undefined // for external reference
  export let hoverEntryId: string | undefined = undefined // for external reference
  export let entryIdKey: SubmodelIdKeys = "nid"

  $: selectedEntryId = $page.url.hash?.replace("#", "") || undefined

  $: browser && scrollEntryIntoView(selectedEntryId)

  onMount(() => scrollEntryIntoView(selectedEntryId))
</script>

{#if entries.length > 0}
  <section class="flex w-full flex-col gap-2">
    {#each entries as entry, index (entry[entryIdKey])}
      {@const idAsString = `${entry[entryIdKey]}`}
      {@const href = selectedEntryId === idAsString ? "" : `#${idAsString}`}

      <article
        id={idAsString}
        class="p-2"
        class:is-selected={selectedEntryId === idAsString}
        class:is-hovered={hoverEntryId === idAsString}
      >
        <h3 class="heading4">
          <a
            class="inline-block w-full"
            {href}
            on:click|preventDefault
            on:mousedown={() => goto(href)}
            on:mouseenter={() => (hoverEntryId = idAsString)}
            on:mouseleave={() => (hoverEntryId = undefined)}
          >
            {index + 1}. {label}
            <small class="text-sm text-gray-500">
              #{idAsString}
            </small>
          </a>
        </h3>
        <slot {entry} />
      </article>
    {/each}
  </section>
{/if}

<style lang="postcss">
  .is-selected {
    @apply animate-fadeToWhite dark:animate-fadeToGray;
  }
  .is-hovered {
    @apply bg-orange-50 dark:bg-gray-700;
  }
</style>
