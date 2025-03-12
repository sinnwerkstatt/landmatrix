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
  import type { SubmodelIdKeys } from "$lib/utils/dataProcessing"
  import { scrollEntryIntoView } from "$lib/utils/domHelpers"

  import SourcesDisplayButton from "$components/Quotations/SourcesDisplayButton.svelte"

  interface Props {
    model: Model
    label: string
    fieldname: SubmodelFieldName
    entries: readonly T[]
    selectedEntryId?: string | undefined // for external reference
    hoverEntryId?: string | undefined // for external reference
    entryIdKey?: SubmodelIdKeys
    children?: Snippet<[T]>
  }

  let {
    model,
    label,
    fieldname,
    entries,
    selectedEntryId = $bindable(undefined),
    hoverEntryId = $bindable(undefined),
    entryIdKey = "nid",
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
    {#each entries as entry, index (entry[entryIdKey])}
      {@const idAsString = `${entry[entryIdKey]}`}
      {@const isSelected = selectedEntryId === idAsString}
      {@const isHovered = hoverEntryId === idAsString}
      {@const href = isSelected ? "" : `#${idAsString}`}

      <article
        id={idAsString}
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
            onmouseenter={() => (hoverEntryId = idAsString)}
            onmouseleave={() => (hoverEntryId = undefined)}
          >
            {index + 1}. {label}
            <small class="text-sm text-gray-500">
              #{idAsString}
            </small>
          </a>
        </h3>
        {#if !isDataSource}
          <div class="my-2">
            <SourcesDisplayButton {model} path={[fieldname, idAsString]} />
          </div>
        {/if}

        {@render children?.(entry)}
      </article>
    {/each}
  </section>
{/if}
