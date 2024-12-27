<script lang="ts">
  interface Extras {
    targetBlank?: boolean
    objectVersion?: number
    model?: "deal" | "investor"
  }

  interface Props {
    value: number
    extras?: Extras
  }

  let { value, extras = {} }: Props = $props()

  let model = $derived(extras.model ?? "deal")
  let href = $derived(
    `/${model}/${value}/${extras.objectVersion ? extras.objectVersion + "/" : ""}`,
  )
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
