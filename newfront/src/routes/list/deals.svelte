<script lang="ts">
  import { _ } from "svelte-i18n";
  import { deals } from "$lib/data";
  import { formfields } from "$lib/stores";
  import { showContextBar, showFilterBar } from "$components/Data";
  import DataContainer from "$components/Data/DataContainer.svelte";
  import FilterCollapse from "$components/Data/FilterCollapse.svelte";
  import DisplayField from "$components/Fields/DisplayField.svelte";
  import Table from "$components/table/Table.svelte";

  let columns = [
    "fully_updated_at",
    "id",
    "country",
    "current_intention_of_investment",
    "operating_company",
  ];

  const allColumns = [
    "fully_updated_at",
    "deal_size",
    "id",
    "country",
    "current_intention_of_investment",
    "current_negotiation_status",
    "current_contract_size",
    "current_implementation_status",
    "intended_size",
    "operating_company",
  ];

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
        {$deals?.length}
      </div>

      <Table sortBy="fully_updated_at" objects={$deals}>
        <thead slot="thead">
          <tr>
            {#each columns as col}
              <th
                class="p-1 sticky top-0 text-white bg-gray-700 font-medium whitespace-nowrap"
                data-sortby={col}
              >
                {$_($formfields.deal[col].label)}
              </th>
            {/each}
          </tr>
        </thead>
        <tbody slot="tbody" let:objects>
          {#each objects as obj}
            <tr class="odd:bg-white even:bg-gray-50 hover:bg-gray-100">
              {#each columns as col}
                <td class="px-1">
                  <DisplayField
                    valueClasses=""
                    wrapperClasses="py-1"
                    showLabel={false}
                    fieldname={col}
                    value={obj[col]}
                  />
                </td>
              {/each}
            </tr>
          {/each}
        </tbody>
      </Table>
    </div>
    <div
      class="flex-none h-full min-h-[3px] {$showContextBar
        ? 'w-[clamp(220px,20%,300px)]'
        : 'w-0'}"
    />
  </div>

  <div slot="FilterBar">
    <FilterCollapse title={$_("Table columns")}>
      <div class="flex flex-col">
        {#each allColumns as opt}
          <label>
            <input type="checkbox" bind:group={columns} value={opt} />
            {$_($formfields.deal[opt]?.label)}
          </label>
        {/each}
      </div>
    </FilterCollapse>
  </div>
</DataContainer>
