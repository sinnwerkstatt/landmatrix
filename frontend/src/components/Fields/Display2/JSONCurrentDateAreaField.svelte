<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { JSONCurrentDateAreaFieldType } from "$lib/types/data"

  import { dateCurrentFormat } from "$components/Fields/Display2/jsonHelpers"

  export let value: JSONCurrentDateAreaFieldType[] = []
</script>

<ul>
  {#each value ?? [] as val}
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
    </li>
  {/each}
</ul>
