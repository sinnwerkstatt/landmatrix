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

<div
  class="jsondatearea_field whitespace-nowrap"
  data-name={formfield ? formfield.name : ""}
>
  {#each value ?? [] as val}
    <div class:font-bold={val.current}>
      <span>{dateCurrentFormat(val)}</span>
      {#if val.area}
        {val.area.toLocaleString("fr")} {$_("ha")}
      {/if}
    </div>
  {/each}
</div>
