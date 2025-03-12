<script lang="ts" module>
  // https://github.com/dummdidumm/rfcs/blob/ts-typedefs-within-svelte-components/text/ts-typing-props-slots-events.md

  import type { SubmodelEntry } from "$lib/utils/dataProcessing"
</script>

<script lang="ts" generics="T extends SubmodelEntry">
  import { onMount, type Snippet } from "svelte"

  import { goto } from "$app/navigation"
  import { page } from "$app/state"

  import type { SubmodelFieldName } from "$lib/fieldLookups"
  import type { Model } from "$lib/types/data"
  import { scrollEntryIntoView } from "$lib/utils/domHelpers"

  import SourcesDisplayButton from "$components/Quotations/SourcesDisplayButton.svelte"

  interface Props {
    model: Model
    label: string
    fieldname: SubmodelFieldName
    entries: readonly T[]
    selectedEntryId?: string | undefined // for external reference
    hoverEntryId?: string | undefined // for external reference
    children?: Snippet<[T]>
  }

  let {
    model,
    label,
    fieldname,
    entries,
    selectedEntryId = $bindable(undefined),
    hoverEntryId = $bindable(undefined),
    children,
  }: Props = $props()

  $effect(() => {
    selectedEntryId = page.url.hash?.replace("#", "") || undefined
  })

  $effect(() => {
    scrollEntryIntoView(selectedEntryId)
  })

  onMount(() => scrollEntryIntoView(selectedEntryId))

  let isDataSource = $derived(fieldname === "datasources")
</script>

{#if entries.length > 0}
  <section class="flex w-full flex-col gap-2">
    {#each entries as entry, index}
      {@const isSelected = selectedEntryId === entry.nid}
      {@const isHovered = hoverEntryId === entry.nid}
      {@const href = isSelected ? "" : `#${entry.nid}`}

      <article
        id={entry.nid}
        class="p-2"
        class:animate-fadeToWhite={isSelected}
        class:dark:animate-fadeToGray={isSelected}
        class:bg-orange-50={isHovered}
        class:dark:bg-gray-700={isHovered}
      >
        <h3 class="heading4">
          <a
            class="inline-block w-full"
            {href}
            onclick={e => e.preventDefault()}
            onmousedown={() => goto(href)}
            onmouseenter={() => (hoverEntryId = entry.nid)}
            onmouseleave={() => (hoverEntryId = undefined)}
          >
            {index + 1}. {label}
            <small class="text-sm text-gray-500">
              #{entry.nid}
            </small>
          </a>
        </h3>
        {#if !isDataSource}
          <div class="my-2">
            <SourcesDisplayButton {model} path={[fieldname, entry.nid]} />
          </div>
        {/if}

        {@render children?.(entry)}
      </article>
    {/each}
  </section>
{/if}
