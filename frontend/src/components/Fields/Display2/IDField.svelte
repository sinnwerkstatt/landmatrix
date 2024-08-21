<script lang="ts">
  export let value: number

  interface Extras {
    targetBlank?: boolean
    objectVersion?: number
    model?: "deal" | "investor"
  }

  export let extras: Extras = {}

  $: model = extras.model ?? "deal"
  $: href = `/${model}/${value}/${extras.objectVersion ? extras.objectVersion + "/" : ""}`
</script>

<a
  class="inline whitespace-nowrap px-2 py-1 text-center align-baseline text-xs font-bold text-white"
  class:deal-id={model === "deal"}
  class:investor-id={model === "investor"}
  {href}
  target={extras.targetBlank ? "_blank" : undefined}
>
  {value}
</a>

<style lang="postcss">
  .deal-id {
    @apply bg-orange hover:bg-orange-600 hover:text-orange-200;
  }
  .investor-id {
    @apply bg-pelorous hover:bg-pelorous-600 hover:text-pelorous-200;
  }
</style>
