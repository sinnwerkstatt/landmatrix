<script lang="ts">
  import cn from "classnames"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: number
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  export let targetBlank = false
  export let objectVersion: number | undefined = undefined
  export let model: "deal" | "investor" = "deal"
</script>

{#if value}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      <a
        class={cn(
          "inline whitespace-nowrap px-2 py-1 text-center align-baseline text-xs font-bold text-white",
          model === "deal"
            ? "bg-orange hover:bg-orange-600"
            : "bg-pelorous hover:bg-pelorous-600 hover:text-pelorous-200",
        )}
        href="/{model}/{value}/{objectVersion ?? ''}"
        target={targetBlank ? "_blank" : undefined}
      >
        {value}
      </a>
    </div>
  </div>
{/if}
