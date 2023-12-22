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
  import DisplayField from "$components/Fields/DisplayField.svelte"
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
    name: 3,
    country: 4,
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

      <div class="h-full w-full border border-gray-700">
        <div class="investor-table grid gap-4 bg-gray-700 py-2 text-white">
          <div>{$_("Last update")}</div>
          <div>{$_("ID")}</div>
          <div>{$_("Name")}</div>
          <div>{$_("Country of registration/origin")}</div>
          <div>{$_("Classification")}</div>
          <div>{$_("Deals")}</div>
        </div>
        <div class="h-full w-full overflow-x-auto">
          {#each $investorsNG as investor}
            <div class="investor-table grid gap-4 odd:bg-gray-200">
              <div class="pb-1 pt-2">
                <DateTimeField
                  fieldname="investor.modified_at"
                  value={investor.selected_version.modified_at}
                />
              </div>
              <div class="pb-1 pt-2">
                <IDField fieldname="investor.id" value={investor.id} model="investor" />
              </div>
              <div class="pb-1 pt-2">
                <TextField
                  fieldname="investor.name"
                  value={investor.selected_version.name}
                />
              </div>
              <div class="pb-1 pt-2">
                <CountryField
                  fieldname="investor.country"
                  value={investor.selected_version.country?.id}
                />
              </div>
              <div class="pb-1 pt-2">
                <TextField
                  fieldname="investor.classification"
                  value={investor.selected_version.classification}
                  choices={$fieldChoices.investor.classification}
                />
              </div>

              <div class="pb-1 pt-2">
                <LengthField
                  fieldname="investor.deals"
                  value={investor.selected_version.deals}
                />
              </div>
            </div>
          {/each}
        </div>
      </div>
      <!--      <Table {columns} items={$investorsNG} {labels} sortBy="-modified_at" {spans}>-->
      <!--        <DisplayField-->
      <!--          fieldname={fieldName}-->
      <!--          let:fieldName-->
      <!--          let:obj-->
      <!--          model="investor"-->
      <!--          slot="field"-->
      <!--          value={obj[fieldName]}-->
      <!--          wrapperClasses="p-1"-->
      <!--        />-->
      <!--      </Table>-->
    </div>
  </div>
  <div slot="FilterBar">
    <h2 class="heading5 my-2 px-2">{$_("Data settings")}</h2>
  </div>
</DataContainer>

<style>
  .investor-table {
  }
</style>
