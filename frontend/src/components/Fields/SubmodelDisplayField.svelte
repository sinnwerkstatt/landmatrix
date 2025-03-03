<script lang="ts" module>
  // https://github.com/dummdidumm/rfcs/blob/ts-typedefs-within-svelte-components/text/ts-typing-props-slots-events.md

  /* eslint-disable-next-line @typescript-eslint/no-unused-vars */
  import type { Submodel } from "$lib/utils/dataProcessing"
</script>

<script lang="ts" generics="T extends Submodel">
  import { onMount, type Snippet } from "svelte"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"
  import { page } from "$app/state"

  import type { Model, SubModelFieldName } from "$lib/types/data"
  import type { SubmodelIdKeys } from "$lib/utils/dataProcessing"
  import { scrollEntryIntoView } from "$lib/utils/domHelpers"

  import DSQuotationsModal from "$components/New/DSQuotationsModal.svelte"

  interface Props {
    model: Model
    label: string
    fieldname: SubModelFieldName
    // eslint-disable-next-line no-undef
    entries: readonly T[]
    selectedEntryId?: string | undefined // for external reference
    hoverEntryId?: string | undefined // for external reference
    entryIdKey?: SubmodelIdKeys
    // eslint-disable-next-line no-undef
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

  let showDSQuotationModal = $state(false)
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
          {@const entryFieldname = `${fieldname}-${idAsString}`}
          {@const quotes =
            page.data[model]?.selected_version.ds_quotations[entryFieldname] ?? []}
          {@const dataSources = page.data[model]?.selected_version.datasources ?? []}

          <div class="mb-2">
            <button
              class="text-lg italic text-purple-400"
              type="button"
              onclick={() => {
                selectedEntryId = idAsString
                showDSQuotationModal = true
              }}
            >
              {$_("Sources")}: {quotes.length}
            </button>

            {#if isSelected && showDSQuotationModal}
              <DSQuotationsModal
                bind:open={showDSQuotationModal}
                {quotes}
                {dataSources}
                label="{label} {idAsString}"
                fieldname={entryFieldname}
              />
            {/if}
          </div>
        {/if}

        {@render children?.(entry)}
      </article>
    {/each}
  </section>
{/if}
