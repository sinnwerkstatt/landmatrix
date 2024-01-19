<script lang="ts">
  import cn from "classnames"

  export let value: number

  interface Extras {
    targetBlank?: boolean
    objectVersion?: number
    model?: "deal" | "investor"
  }

  export let extras: Extras = {}

  $: model = extras.model ?? "deal"
</script>

<a
  class={cn(
    "inline whitespace-nowrap px-2 py-1 text-center align-baseline text-xs font-bold text-white",
    model === "deal"
      ? "bg-orange hover:bg-orange-600"
      : "bg-pelorous hover:bg-pelorous-600 hover:text-pelorous-200",
  )}
  href="/{model}/{value}/{extras.objectVersion ?? ''}"
  target={extras.targetBlank ? "_blank" : undefined}
>
  {value}
</a>
