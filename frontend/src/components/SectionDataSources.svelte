<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import type { DealVersion2, InvestorVersion2 } from "$lib/types/newtypes"
  import { isElementInViewport } from "$lib/utils/domHelpers"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let version: DealVersion2 | InvestorVersion2

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

{#if version.datasources.length > 0}
  <section class="w-full">
    {#each version.datasources as datasource, index}
      <div
        id={datasource.nid}
        class="p-2 {selectedEntryId === datasource.nid
          ? 'animate-fadeToWhite dark:animate-fadeToGray'
          : ''}"
      >
        <div class="heading4">
          <a href="#{datasource.nid}">
            {index + 1}. {$_("Data source")}
          </a>
        </div>
        <DisplayField fieldname="datasource.nid" showLabel value={datasource.nid} />
        <DisplayField fieldname="datasource.type" showLabel value={datasource.type} />
        <DisplayField fieldname="datasource.url" showLabel value={datasource.url} />
        <DisplayField
          fieldname="datasource.file"
          showLabel
          value={datasource.file}
          extras={{ notPublic: datasource.file_not_public }}
        />
        <DisplayField
          fieldname="datasource.publication_title"
          showLabel
          value={datasource.publication_title}
        />
        <DisplayField fieldname="datasource.date" showLabel value={datasource.date} />
        <DisplayField fieldname="datasource.name" showLabel value={datasource.name} />
        <DisplayField
          fieldname="datasource.company"
          showLabel
          value={datasource.company}
        />
        <DisplayField fieldname="datasource.email" showLabel value={datasource.email} />
        <DisplayField fieldname="datasource.phone" showLabel value={datasource.phone} />
        <DisplayField
          fieldname="datasource.includes_in_country_verified_information"
          showLabel
          value={datasource.includes_in_country_verified_information}
        />
        <DisplayField
          fieldname="datasource.open_land_contracts_id"
          showLabel
          value={datasource.open_land_contracts_id}
        />
        <DisplayField
          fieldname="datasource.comment"
          showLabel
          value={datasource.comment}
        />
      </div>
    {/each}
  </section>
{/if}
