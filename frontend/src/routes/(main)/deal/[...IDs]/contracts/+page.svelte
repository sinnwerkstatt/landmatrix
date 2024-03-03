<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import type { DealVersion2 } from "$lib/types/newtypes"
  import { isElementInViewport } from "$lib/utils/domHelpers"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let data

  let version: DealVersion2 = data.deal.selected_version
  $: version = data.deal.selected_version

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

{#if version.contracts.length > 0}
  <section class="w-full">
    {#each version.contracts as contract, index}
      <div
        id={contract.nid}
        class="p-2 {selectedEntryId === contract.nid
          ? 'animate-fadeToWhite dark:animate-fadeToGray'
          : ''}"
      >
        <div class="heading4">
          <a href="#{contract.nid}">
            {index + 1}. {$_("Contract")}
          </a>
        </div>
        <DisplayField fieldname="contract.nid" showLabel value={contract.nid} />
        <DisplayField fieldname="contract.number" showLabel value={contract.number} />
        <DisplayField fieldname="contract.date" showLabel value={contract.date} />
        <DisplayField
          fieldname="contract.expiration_date"
          showLabel
          value={contract.expiration_date}
        />
        <DisplayField
          fieldname="contract.agreement_duration"
          showLabel
          value={contract.agreement_duration}
        />
        <DisplayField fieldname="contract.comment" showLabel value={contract.comment} />
      </div>
    {/each}
  </section>
{/if}
