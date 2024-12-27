<script lang="ts">
  import { twMerge } from "tailwind-merge"

  interface Props {
    value: string
    class?: string
  }

  let { value, class: className = "" }: Props = $props()
</script>

<div class={twMerge("flex items-center gap-2 font-medium", className)}>
  {value}
</div>
