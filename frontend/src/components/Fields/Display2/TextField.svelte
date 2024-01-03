<script lang="ts">
  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: string | string[]
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  export let url = false
  export let multipleChoices = false
  export let choices: { value: string; label: string }[] = []

  const isMulti = (value: string | string[]): value is string[] => multipleChoices
  const isUrl = (value: string | string[]): value is string => url

  function enrichValue(value: string | string[]) {
    if (!value) return "—"
    if (isMulti(value)) {
      if (choices.length > 0)
        return value.map(x => choices.find(c => c.value === x)?.label ?? "-").join(", ")
      else return value.join(", ")
    } else {
      if (choices.length > 0) return choices.find(c => c.value === value)?.label ?? ""
      else return value
    }
  }
</script>

{#if value}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      {#if isUrl(value)}
        <a href={value} target="_blank" rel="noreferrer">{new URL(value).hostname}</a>
      {:else}
        {enrichValue(value)}
      {/if}
    </div>
  </div>
{/if}
