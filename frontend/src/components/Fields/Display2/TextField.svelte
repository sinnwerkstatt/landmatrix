<script lang="ts">
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: string
  export let fieldname: string
  export let label = ""
  export let hideLabel = false
  export let url = false
</script>

{#if value}
  <div class="mb-3 flex flex-wrap leading-5" data-fieldname={fieldname}>
    {#if !hideLabel}
      <Label2 value={label} class="md:w-5/12 lg:w-4/12" />
    {/if}
    <div class="text-lm-dark dark:text-white md:w-7/12 lg:w-8/12">
      {#if !value}
        —
      {:else if url}
        <a href={value} target="_blank" rel="noreferrer">{new URL(value).hostname}</a>
      {:else}
        {value}
      {/if}
    </div>
  </div>
{/if}
