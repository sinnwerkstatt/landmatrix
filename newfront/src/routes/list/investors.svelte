<script lang="ts">
  import { _ } from "svelte-i18n";
  import { investors } from "$lib/data";
  import { formfields } from "$lib/stores";
  import { showContextBar, showFilterBar } from "$components/Data";
  import DataContainer from "$components/Data/DataContainer.svelte";
  import DisplayField from "$components/Fields/DisplayField.svelte";
  import Table from "$components/table/Table.svelte";

  let columns = ["modified_at", "id", "name", "country", "classification", "deals"];

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

      <Table sortBy="modified_at" objects={$investors}>
        <thead slot="thead">
          <tr>
            {#each columns as col}
              <th
                class="p-1 sticky top-0 text-white bg-gray-700 font-medium whitespace-nowrap"
                data-sortby={col}
              >
                {$_($formfields.investor[col].label)}
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
                    fieldname={col}
                    model="investor"
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
