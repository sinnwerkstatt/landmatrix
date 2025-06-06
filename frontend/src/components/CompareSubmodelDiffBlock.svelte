<script lang="ts">
  import { diff } from "deep-object-diff"

  import { dealFields, investorFields } from "$lib/fieldLookups"
  import { isNotEmpty } from "$lib/helpers"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  interface Props {
    fromObjs: { nid: string; [key: string]: unknown }[]
    toObjs: { nid: string; [key: string]: unknown }[]
    heading: string
    label: string
    lookupString: string
    model?: "deal" | "investor"
  }

  let {
    fromObjs,
    toObjs,
    heading,
    label,
    lookupString,
    model = "deal",
  }: Props = $props()

  const IGNORE_KEYS = ["nid"]

  const objNIDs = new Set([...fromObjs.map(l => l.nid), ...toObjs.map(l => l.nid)])

  let fieldLookup = $derived(model === "deal" ? $dealFields : $investorFields)
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

    {#each Object.keys(hasDiff).filter(k => !IGNORE_KEYS.includes(k)) as key}
      {@const fieldname = `${lookupString}.${key}`}

      {#if (fromL && isNotEmpty(fromL[key])) || (toL && isNotEmpty(toL[key]))}
        <tr>
          <th>
            {fieldLookup[fieldname]?.label ?? key}
          </th>
          <td>
            {#if fromL}
              <DisplayField
                {fieldname}
                {model}
                value={fromL[key]}
                wrapperClass="py-2"
                valueClass=""
              />
            {/if}
          </td>
          <td>
            {#if toL}
              <DisplayField
                {fieldname}
                {model}
                value={toL[key]}
                wrapperClass="py-2"
                valueClass=""
              />
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
    @apply border-b border-r p-2;

    :global {
      @apply dark:border-gray-100;
    }
  }

  th:first-child {
    @apply border-l;

    :global {
      @apply dark:border-gray-100;
    }
  }

  h2 {
    @apply my-0 text-center text-lg text-white md:text-xl xl:text-2xl;
  }

  h3 {
    @apply my-0 text-sm md:text-base xl:text-lg;
  }
</style>
