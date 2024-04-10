<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { investorFields } from "$lib/fieldLookups"
  import { investorsNG } from "$lib/stores"
  import { isMobile } from "$lib/stores/basics"

  import DataContainer from "$components/Data/DataContainer.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Table from "$components/Table/Table.svelte"

  const COLUMNS = [
    { key: "modified_at", colSpan: 2 },
    { key: "id", colSpan: 1 },
    { key: "name", colSpan: 5 },
    { key: "country", colSpan: 5 },
    { key: "classification", colSpan: 3 },
    { key: "deals", colSpan: 1 },
  ]

  $: columns = COLUMNS.map(x => x.key)
  $: labels = COLUMNS.map(x => $investorFields[x.key].label)
  $: spans = COLUMNS.map(x => x.colSpan)

  onMount(() => {
    showContextBar.set(false)
    showFilterBar.set(!$isMobile)
  })
  const wrapperClass = "p-1"
  const valueClass = ""
</script>

<svelte:head>
  <title>{$_("Investors")} | {$_("Land Matrix")}</title>
</svelte:head>

<DataContainer>
  <div class="flex h-full">
    <div
      class="h-full min-h-[3px] w-0 flex-none {$showFilterBar
        ? 'md:w-[clamp(220px,20%,300px)]'
        : ''}"
    />

    <div class="flex h-full w-1 grow flex-col px-6 pb-6">
      <div class="flex h-20 items-center text-lg">
        {$investorsNG?.length ?? "—"}
        {$investorsNG?.length === 1 ? $_("Investor") : $_("Investors")}
      </div>

      <Table {columns} items={$investorsNG} {labels} sortBy="-modified_at" {spans}>
        <svelte:fragment let:fieldName let:obj slot="field">
          {#if ["id", "deals"].includes(fieldName)}
            <DisplayField
              fieldname={fieldName}
              value={obj[fieldName]}
              model="investor"
              {wrapperClass}
              {valueClass}
            />
          {:else}
            <DisplayField
              fieldname={fieldName}
              value={obj.selected_version[fieldName]}
              model="investor"
              {wrapperClass}
              {valueClass}
            />
          {/if}
        </svelte:fragment>
      </Table>
    </div>
  </div>
  <div slot="FilterBar">
    <h2 class="heading5 my-2 px-2">{$_("Data settings")}</h2>
  </div>
</DataContainer>
