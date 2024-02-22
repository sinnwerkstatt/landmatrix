<script lang="ts">
  import { dealFields, investorFields } from "$lib/fieldLookups"

  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: unknown | null
  export let fieldname: string
  export let wrapperClass = "mb-10 leading-5 flex flex-col"
  export let labelClass = "font-semibold mb-4 w-full"
  export let valueClass = "text-lm-dark dark:text-white w-full"

  export let showLabel = false
  export let model: "deal" | "investor" = "deal"

  export let extras: unknown | undefined = undefined

  $: richField = model === "deal" ? $dealFields[fieldname] : $investorFields[fieldname]

  let allExtras: unknown
  $: allExtras =
    richField?.extras && extras
      ? { ...richField.extras, ...extras }
      : richField?.extras ?? extras
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  <!-- TODO Later Nuts wrap content into label -->
  {#if showLabel}
    <Label2 value={richField?.label} class={labelClass} />
  {/if}
  <div class={valueClass}>
    {#if richField && richField.editField}
      {#if allExtras}
        {#if $$slots.default}
          <svelte:component
            this={richField.editField}
            bind:value
            extras={allExtras}
            {fieldname}
          >
            <slot />
          </svelte:component>
        {:else}
          <svelte:component
            this={richField.editField}
            bind:value
            extras={allExtras}
            {fieldname}
          />
        {/if}
      {:else if $$slots.default}
        <svelte:component this={richField.editField} bind:value {fieldname}>
          <slot />
        </svelte:component>
      {:else}
        <svelte:component this={richField.editField} bind:value {fieldname} />
      {/if}
    {:else}
      <div class="italic text-red-400">unknown field</div>
    {/if}
  </div>
</div>
