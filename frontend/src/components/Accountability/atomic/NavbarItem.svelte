<script lang="ts">
  import type { Component } from "svelte"

  import { page } from "$app/state"

  interface Props {
    label?: string
    href?: string
    icon: Component
  }

  let { label = "Item", href = "/accountability/", icon }: Props = $props()

  const IconComp = $derived(icon)
  const active = $derived(page.url.pathname.startsWith(href))
</script>

<a
  {href}
  class:active
  class="group flex flex-col items-center gap-1 text-a-s font-semibold text-a-gray-900 hover:text-a-gray-900"
>
  <span
    class="icon rounded-lg p-2 group-hover:bg-a-gray-100"
    class:bg-a-gray-100={active}
  >
    <IconComp />
  </span>
  <span>{label}</span>
</a>
