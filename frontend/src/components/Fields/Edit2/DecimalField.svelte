<script lang="ts">
  import Label2 from "$components/Fields/Display2/Label2.svelte"
  import LowLevelDecimalField from "$components/Fields/Edit/LowLevelDecimalField.svelte"

  export let value: number | null
  export let fieldname: string
  export let label = ""
  export let wrapperClass = "mb-3 flex flex-wrap leading-5"
  export let labelClass = "md:w-5/12 lg:w-4/12"
  export let valueClass = "text-lm-dark dark:text-white md:w-7/12 lg:w-8/12"
  export let unit: string | undefined = undefined
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if label}
    <Label2 value={label} class={labelClass} />
  {/if}
  <div class={valueClass}>
    <LowLevelDecimalField bind:value name={fieldname} {unit} />
  </div>
</div>
