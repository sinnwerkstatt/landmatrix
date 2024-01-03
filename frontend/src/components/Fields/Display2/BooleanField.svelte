<script lang="ts">
  import { _ } from "svelte-i18n"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: boolean | null
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS
</script>

{#if value !== null}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      {#if value === true}
        {$_("Yes")}
      {:else if value === false}
        {$_("No")}
      {:else}
        —
      {/if}
    </div>
  </div>
{/if}
