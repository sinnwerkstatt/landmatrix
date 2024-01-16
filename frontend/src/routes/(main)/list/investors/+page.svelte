<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { fieldChoices, formfields, investorsNG, isMobile } from "$lib/stores"

  import DataContainer from "$components/Data/DataContainer.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import CountryField from "$components/Fields/Display2/CountryField.svelte"
  import DateTimeField from "$components/Fields/Display2/DateTimeField.svelte"
  import IDField from "$components/Fields/Display2/IDField.svelte"
  import LengthField from "$components/Fields/Display2/LengthField.svelte"
  import TextField from "$components/Fields/Display2/TextField.svelte"
  import Table from "$components/Table/Table.svelte"

  const COLUMNS = [
    "modified_at",
    "id",
    "name",
    "country",
    "classification",
    "deals",
  ] as const

  type ColumnName = (typeof COLUMNS)[number]

  const columnSpanMap: { [key in ColumnName]: number } = {
    modified_at: 2,
    id: 1,
    name: 5,
    country: 5,
    classification: 4,
    deals: 1,
  }

  $: columns = COLUMNS.map(col => col)
  $: labels = COLUMNS.map(col => $formfields.investor[col].label)
  $: spans = COLUMNS.map(col => columnSpanMap[col])

  onMount(() => {
    showContextBar.set(false)
    showFilterBar.set(!$isMobile)
  })
</script>

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
        <svelte:fragment slot="field" let:obj let:fieldName>
          {#if fieldName === "modified_at"}
            <DateTimeField
              fieldname="investor.modified_at"
              value={obj.selected_version.modified_at}
              wrapperClass="p-1"
            />
          {:else if fieldName === "id"}
            <IDField
              fieldname="investor.id"
              value={obj.id}
              model="investor"
              wrapperClass="p-1"
            />
          {:else if fieldName === "name"}
            {#if obj.selected_version.name_unknown}
              <span class="italic text-gray-600">[{$_("unknown investor")}]</span>
            {:else}
              {obj.selected_version.name}
            {/if}
          {:else if fieldName === "country"}
            <CountryField
              fieldname="investor.country"
              value={obj.selected_version.country?.id}
            />
          {:else if fieldName === "classification"}
            <TextField
              fieldname="investor.classification"
              value={obj.selected_version.classification}
              choices={$fieldChoices.investor.classification}
            />
          {:else}
            <LengthField
              fieldname="investor.deals"
              value={obj.selected_version.deals}
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
