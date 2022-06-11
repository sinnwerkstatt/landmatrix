<script lang="ts">
  import { afterNavigate } from "$app/navigation";
  import { deals } from "$lib/data";
  import { formfields } from "$lib/stores.js";
  import { showContextBar, showFilterBar } from "$components/Data";
  import DataContainer from "$components/Data/DataContainer.svelte";
  import DisplayField from "$components/Fields/DisplayField.svelte";
  import Table from "$components/table/Table.svelte";

  const columns = [
    "fully_updated_at",
    "id",
    "country",
    "current_intention_of_investment",
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

      <Table objects={$deals}>
        <thead slot="thead">
          <tr>
            {#each columns as col}
              <th class="p-1 sticky top-0 text-white bg-gray-700 font-medium">
                {$formfields.deal[col].label}
              </th>
            {/each}
          </tr>
        </thead>
        <tbody slot="tbody" let:objects>
          {#each objects as obj}
            <tr class="odd:bg-white even:bg-gray-50 hover:bg-gray-100 px-1 py-3">
              {#each columns as col}
                <td>
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
</DataContainer>
