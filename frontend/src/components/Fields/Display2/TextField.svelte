<script lang="ts">
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: string
  export let fieldname: string
  export let label = ""
  export let wrapperClass = "mb-3 flex flex-wrap leading-5"
  export let labelClass = "md:w-5/12 lg:w-4/12"
  export let valueClass = "text-lm-dark dark:text-white md:w-7/12 lg:w-8/12"

  export let url = false
  export let multipleChoices = false
  export let choices: { value: string; label: string }[] | undefined = undefined
</script>

{#if value}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      {#if !value}
        —
      {:else if choices}
        {#if multipleChoices}
          {#each value as v}
            {choices.find(c => c.value === v)?.label ?? ""}
          {/each}
        {:else}
          {choices.find(c => c.value === value)?.label ?? "-"}
        {/if}
      {:else if url}
        <a href={value} target="_blank" rel="noreferrer">{new URL(value).hostname}</a>
      {:else}
        {value}
      {/if}
    </div>
  </div>
{/if}
