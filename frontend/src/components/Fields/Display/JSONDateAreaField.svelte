<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dateCurrentFormat } from "$components/Fields/Display/jsonHelpers"
  import type { FormField } from "$components/Fields/fields"

  type JSONDateAreaFieldType = {
    area: string
    date: string
    current?: boolean
  }

  export let formfield: FormField
  export let value: JSONDateAreaFieldType[] = []
</script>

<ul>
  {#each value ?? [] as val}
    <li class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>
      {#if val.area}
        {val.area.toLocaleString("fr")} {$_("ha")}
      {/if}
    </li>
  {/each}
</ul>
