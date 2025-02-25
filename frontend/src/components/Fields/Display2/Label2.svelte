<script lang="ts">
  import { twMerge } from "tailwind-merge"

  import ContextHelper from "$components/ContextHelper.svelte"

  interface Props {
    value: string
    class?: string
    contextHelp?: string
  }

  let { value, class: className = "", contextHelp }: Props = $props()
</script>

<div class={twMerge("flex items-center gap-2 font-medium", className)}>
  {value}
  {#if contextHelp}
    <ContextHelper identifier={contextHelp} />
  {/if}
</div>
