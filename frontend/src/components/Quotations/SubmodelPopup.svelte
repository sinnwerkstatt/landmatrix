<script lang="ts" module>
  import type { Component } from "svelte"

  import type { SubmodelEntry } from "$lib/utils/dataProcessing"

  import ContractPopup from "$components/Quotations/ContractPopup.svelte"
  import DataSourcePopup from "$components/Quotations/DataSourcePopup.svelte"
  import InvolvementPopup from "$components/Quotations/InvolvementPopup.svelte"
  import LocationPopup from "$components/Quotations/LocationPopup.svelte"
  import type { SubmodelKey } from "$components/Quotations/ReviewChangesModal.svelte"

  const POPUP_MAP: { [key in SubmodelKey]: Component<any, any, any> } = {
    locations: LocationPopup,
    datasources: DataSourcePopup,
    contracts: ContractPopup,
    involvements: InvolvementPopup,
  }
</script>

<script lang="ts" generics="T extends SubmodelEntry">
  import { createFloatingActions } from "svelte-floating-ui"
  import { autoPlacement, offset, shift } from "svelte-floating-ui/dom"

  import InfoIcon from "$components/icons/InfoIcon.svelte"

  interface Props {
    key: SubmodelKey
    entry: T
    label: string
  }

  let { key, entry, label }: Props = $props()

  let showTooltip = $state(false)

  const [floatingRef, floatingContent] = createFloatingActions({
    strategy: "absolute",
    middleware: [offset(10), shift(), autoPlacement()],
  })
</script>

<span
  class="p-2"
  role="presentation"
  aria-hidden="true"
  onmouseenter={() => (showTooltip = true)}
  onmouseleave={() => (showTooltip = false)}
  use:floatingRef
>
  <InfoIcon />
</span>

{#if showTooltip}
  {@const PopupComp = POPUP_MAP[key]}
  <div
    class="absolute w-96 border-2 bg-white p-4 drop-shadow-2xl dark:bg-gray-900 dark:text-white"
    use:floatingContent
  >
    <h5 class="heading5">
      {label}
      <small class="text-sm text-gray-500">
        #{entry.nid}
      </small>
    </h5>

    <PopupComp {entry} />
  </div>
{/if}
