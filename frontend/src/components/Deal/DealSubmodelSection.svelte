<script lang="ts">
  import cn from "classnames"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { isEmpty } from "$lib/helpers"
  import { subsections } from "$lib/sections"
  import type { Contract, DataSource, Location } from "$lib/types/deal"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let model: string
  export let modelName: string
  export let entries: Array<Contract | DataSource | Location> = []

  let fields: string[]
  $: fields = subsections[model]

  let nanoIDHighlight: string | undefined
  $: nanoIDHighlight = $page.url.hash.split("/")?.[1]

  onMount(() => {
    if (nanoIDHighlight) document.getElementById(nanoIDHighlight)?.scrollIntoView()
  })
</script>

{#if entries?.length > 0}
  <section class="flex h-full flex-wrap">
    <div class={$$slots.default ? "w-full lg:w-1/2" : "w-full"}>
      {#each entries as entry, index}
        <div
          id={entry.id}
          class={cn(
            `${model}-entry`,
            nanoIDHighlight === entry.id ? "animate-fadeToWhite bg-orange-100" : "",
          )}
        >
          <h3>
            {index + 1}. {$_(modelName)}
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
              />
            {/if}
          {/each}
        </div>
      {/each}
    </div>
    <slot />
  </section>
{/if}
