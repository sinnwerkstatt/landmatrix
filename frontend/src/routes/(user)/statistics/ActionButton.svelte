<script lang="ts">
  import type { Component } from "svelte"
  import type { MouseEventHandler } from "svelte/elements"

  interface Props {
    label: string
    icon: Component
    highlight?: boolean
    onclick?: MouseEventHandler<HTMLButtonElement>
  }

  let { label, icon, highlight = false, onclick }: Props = $props()

  const SvelteComponent = $derived(icon)
</script>

<button
  class="group flex items-center gap-3 rounded-full p-1 transition-colors hover:bg-gray-50 hover:text-orange dark:hover:bg-gray-700"
  class:text-violet={highlight}
  {onclick}
  type="button"
>
  <SvelteComponent class="size-8 transition-colors" />
  <span class="text-2xl transition-colors">
    {label}
  </span>
</button>
