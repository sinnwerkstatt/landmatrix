<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { JSONCurrentDateAreaFieldType } from "$lib/types/data"

  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"
  import SourcesDisplayButton from "$components/Quotations/SourcesDisplayButton.svelte"

  interface Props {
    value?: JSONCurrentDateAreaFieldType[]
    fieldname?: string
  }

  let { value = [], fieldname = "" }: Props = $props()
</script>

<ul>
  {#each value ?? [] as val, i}
    <li class:font-semibold={val.current}>
      <span>{dateCurrentFormat(val)}</span>

      <!-- The literal translation strings are defined in apps/landmatrix/models/choices.py -->
      <!--{val.choices.map(v => $_(flat_choices[v])).join(", ")}-->
      {#if val.area}
        <span class="text-[1.1em]">
          {val.area.toLocaleString("fr").replace(",", ".")}
          {$_("ha")}
        </span>
      {/if}

      <SourcesDisplayButton path={[fieldname, i]} />
    </li>
  {/each}
</ul>
