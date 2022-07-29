<script lang="ts">
  import { _ } from "svelte-i18n";
  import { investors } from "$lib/data";
  import { formfields } from "$lib/stores";
  import { showContextBar, showFilterBar } from "$components/Data";
  import DataContainer from "$components/Data/DataContainer.svelte";
  import DisplayField from "$components/Fields/DisplayField.svelte";
  import Table from "$components/table/Table.svelte";

  const allColumnsWithSpan = {
    modified_at: 2,
    id: 1,
    name: 3,
    country: 3,
    classification: 4,
    deals: 1,
  };

  $: columns = Object.keys(allColumnsWithSpan);
  $: labels = columns.map((col) => $formfields.investor[col].label);
  $: spans = Object.entries(allColumnsWithSpan).map(([_, colSpan]) => colSpan);

  showContextBar.set(false);
</script>

<DataContainer>
  <div class="h-full flex">
    <div
      class="flex-none h-full min-h-[3px] {$showFilterBar
        ? 'w-[clamp(220px,20%,300px)]'
        : 'w-0'}"
    />

    <div class="px-4 bg-stone-100 w-full flex flex-col">
      <div class="h-[4rem] flex items-center pl-2 text-lg">
        {$investors?.length ?? "—"}
        {$investors?.length === 1 ? $_("Investor") : $_("Investors")}
      </div>

      <Table sortBy="-modified_at" items={$investors} {columns} {spans} {labels}>
        <DisplayField
          slot="field"
          let:fieldName
          let:fieldValue
          model="investor"
          wrapperClasses="p-1"

          fieldname={fieldName}
          value={fieldValue}
        />
      </Table>
    </div>
    <div
      class="flex-none h-full min-h-[3px] {$showContextBar
        ? 'w-[clamp(220px,20%,300px)]'
        : 'w-0'}"
    />
  </div>
</DataContainer>
