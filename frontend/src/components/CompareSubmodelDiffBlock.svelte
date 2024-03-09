<script lang="ts">
  import { diff } from "deep-object-diff"
  import { _ } from "svelte-i18n"

  import { dealFields } from "$lib/fieldLookups"
  import { isNotEmpty } from "$lib/helpers"

  import InvestorLinkField from "$components/Fields/Display2/InvestorLinkField.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let fromObjs: { nid: string; [key: string]: unknown }[]
  export let toObjs: { nid: string; [key: string]: unknown }[]

  export let heading: string
  export let label: string
  export let lookupString: string

  export let useInvoID = false

  $: objNIDs = useInvoID
    ? new Set([...fromObjs.map(l => l.id), ...toObjs.map(l => l.id)])
    : new Set([...fromObjs.map(l => l.nid), ...toObjs.map(l => l.nid)])
</script>

<tr class="hidden bg-gray-700 [&:has(+.🍏)]:table-row">
  <th colspan="3">
    <h2>{heading}</h2>
  </th>
</tr>

{#each objNIDs as dsNID}
  {@const fromL = fromObjs.find(l => l.nid === dsNID)}
  {@const toL = toObjs.find(l => l.nid === dsNID)}
  {@const hasDiff = diff(fromL ?? {}, toL ?? {})}
  {#if Object.keys(hasDiff).length}
    <tr class="🍏 bg-gray-100 dark:bg-gray-600">
      <th colspan="3">
        <h3>{label} #{dsNID ?? ""}</h3>
      </th>
    </tr>
    {#each Object.keys(hasDiff) as key}
      {#if (fromL && isNotEmpty(fromL[key])) || (toL && isNotEmpty(toL[key]))}
        <tr>
          <td>
            {#if key === "other_investor"}
              {$_("Investor")}
            {:else}
              {$dealFields[`${lookupString}.${key}`]?.label ?? key}
            {/if}
          </td>
          <td>
            {#if fromL}
              <DisplayField
                fieldname="{lookupString}.{key}"
                value={fromL[key]}
                wrapperClass="py-2"
              />
            {/if}
          </td>
          <td>
            {#if toL}
              {#if key === "other_investor"}
                <InvestorLinkField value={toL.other_investor?.id} />
              {:else}
                <DisplayField
                  fieldname="{lookupString}.{key}"
                  value={toL[key]}
                  wrapperClass="py-2"
                />
              {/if}
            {/if}
          </td>
        </tr>
      {/if}
    {/each}
  {/if}
{/each}

<!--TODO Later: Include in class tag after refactoring component logic-->
<style lang="postcss">
  td,
  th {
    @apply border-b border-r p-2 dark:border-gray-100;
  }

  th:first-child {
    @apply border-l dark:border-gray-100;
  }

  h2 {
    @apply my-0 text-center text-lg text-white md:text-xl xl:text-2xl;
  }

  h3 {
    @apply my-0 text-sm md:text-base xl:text-lg;
  }
</style>
