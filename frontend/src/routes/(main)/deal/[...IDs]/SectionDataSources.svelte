<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import type { DealVersion2 } from "$lib/types/newtypes"
  import { isElementInViewport } from "$lib/utils/domHelpers"

  import NanoIDField from "$components/Fields/Display2/NanoIDField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"

  export let version: DealVersion2

  let selectedEntryId: string | undefined
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

{#if version.datasources.length > 0}
  <section class="w-full">
    {#each version.datasources as datasource, index}
      <div
        id={datasource.nid}
        class="p-2 {selectedEntryId === datasource.nid
          ? 'animate-fadeToWhite dark:animate-fadeToGray'
          : ''}"
      >
        <h3>
          <a href={$page.url.hash.split("/")[0] + `/${datasource.nid}`}>
            {index + 1}. {$_("Data source")}
          </a>
        </h3>
        <NanoIDField
          value={datasource.nid}
          label={$_("ID")}
          fieldname="datasource.nid"
        />
        <TextField
          value={datasource.type}
          label={$_("Type")}
          fieldname="datasource.type"
        />
        <TextField
          value={datasource.url}
          label={$_("Url")}
          fieldname="datasource.url"
          url
        />
      </div>
    {/each}
  </section>
{/if}
