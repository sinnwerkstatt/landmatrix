<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"
  import { browser } from "$app/environment"

  import { isEmpty } from "$lib/helpers"
  import { subsections } from "$lib/sections"
  import type { Contract, DataSource, Location } from "$lib/types/deal"
  import { isElementInViewport } from "$lib/utils/domHelpers"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  type Entry = Contract | DataSource | Location

  export let model: string
  export let modelName: string
  export let entries: Entry[] = []

  let fields: string[]
  $: fields = subsections[model]

  export let selectedEntryId: string | undefined
  $: selectedEntryId = $page.url.hash.split("/")?.[1]
  $: browser && scrollEntryIntoView(selectedEntryId)

  const scrollEntryIntoView = (id: string | undefined) => {
    const el = document.getElementById(id ?? "")
    if (el && !isElementInViewport(el)) {
      el.scrollIntoView({ block: "nearest", inline: "nearest" })
    }
  }

  onMount(() => scrollEntryIntoView(selectedEntryId))
</script>

{#if entries?.length > 0}
  <section class="w-full">
    {#each entries as entry, index}
      <div id={entry.id} class={"p-2"} class:selected={selectedEntryId === entry.id}>
        <h3>
          <a href={$page.url.hash.split("/")[0] + `/${entry.id}`}>
            {index + 1}. {$_(modelName)}
          </a>
        </h3>
        <DisplayField fieldname="id" value={entry["id"]} {model} showLabel />
        {#each fields as fieldname}
          {#if !isEmpty(entry[fieldname])}
            <DisplayField
              {fieldname}
              value={entry[fieldname]}
              {model}
              showLabel
              fileNotPublic={entry.file_not_public}
              on:toggleVisibility
            />
          {/if}
        {/each}
      </div>
    {/each}
  </section>
{/if}

<style lang="css">
  .selected {
    @apply animate-fadeToWhite dark:animate-fadeToGray;
  }
</style>
