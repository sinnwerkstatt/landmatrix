<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { investorFields } from "$lib/fieldLookups"
  import { investorsNG } from "$lib/stores"
  import { isMobile } from "$lib/stores/basics"

  import DataContainer from "$components/Data/DataContainer.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Table, { type Column } from "$components/Table/Table.svelte"

  let columns: Column[]
  $: columns = [
    { key: "modified_at", colSpan: 2, submodel: "selected_version" },
    { key: "id", colSpan: 1 },
    { key: "name", colSpan: 5, submodel: "selected_version" },
    { key: "country_id", colSpan: 5, submodel: "selected_version" },
    { key: "classification", colSpan: 3, submodel: "selected_version" },
    { key: "deals", colSpan: 1 },
  ].map(c => ({ ...c, label: $investorFields[c.key].label }))

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

      <Table {columns} items={$investorsNG} sortBy="-modified_at">
        <svelte:fragment let:fieldName let:obj slot="field">
          {@const col = columns.find(c => c.key === fieldName)}
          <DisplayField
            fieldname={col.key}
            value={col.submodel ? obj[col.submodel][col.key] : obj[col.key]}
            model="investor"
            {wrapperClass}
            {valueClass}
          />
        </svelte:fragment>
      </Table>
    </div>
  </div>
  <div slot="FilterBar">
    <h2 class="heading5 my-2 px-2">{$_("Data settings")}</h2>
  </div>
</DataContainer>
