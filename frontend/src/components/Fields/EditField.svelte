<script lang="ts">
  import type { Snippet } from "svelte"

  import { dealFields, investorFields } from "$lib/fieldLookups"

  import Label2 from "$components/Fields/Display2/Label2.svelte"

  interface Props {
    value: unknown | null
    fieldname: string
    wrapperClass?: string
    labelClass?: string
    valueClass?: string
    showLabel?: boolean
    model?: "deal" | "investor"
    extras?: unknown | undefined
    children?: Snippet
  }

  let {
    value = $bindable(),
    fieldname,
    wrapperClass = "mb-10 leading-5 flex flex-col",
    labelClass = "font-semibold mb-4 w-full",
    valueClass = "text-gray-700 dark:text-white w-full",
    showLabel = false,
    model = "deal",
    extras = undefined,
    children,
  }: Props = $props()

  let richField = $derived(
    model === "deal" ? $dealFields[fieldname] : $investorFields[fieldname],
  )

  let allExtras: unknown = $derived(
    richField?.extras && extras
      ? { ...richField.extras, ...extras }
      : (richField?.extras ?? extras),
  )
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if showLabel}
    <Label2 value={richField?.label} class={labelClass} />
  {/if}
  <div class={valueClass}>
    {#if richField && richField.editField}
      {#if allExtras}
        {#if children}
          <richField.editField bind:value extras={allExtras} {fieldname}>
            {@render children?.()}
          </richField.editField>
        {:else}
          <richField.editField bind:value extras={allExtras} {fieldname} />
        {/if}
      {:else if children}
        <richField.editField bind:value {fieldname}>
          {@render children?.()}
        </richField.editField>
      {:else}
        <richField.editField bind:value {fieldname} />
      {/if}
    {:else}
      <div class="italic text-red-400">unknown field: {fieldname}</div>
    {/if}
  </div>
</div>
