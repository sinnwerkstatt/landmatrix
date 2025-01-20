<script lang="ts">
  import { page } from "$app/stores"

  interface Props {
    label?: string
    href?: string
    icon?: import("svelte").Snippet
  }

  let { label = "Item", href = "/accountability/", icon }: Props = $props()
</script>

<a
  {href}
  class:active={$page.url.pathname.startsWith(href)}
  class="flex flex-col items-center gap-1 text-a-s font-semibold text-a-gray-900 hover:text-a-gray-900"
>
  <span class="icon rounded-lg p-2">
    {@render icon?.()}
  </span>
  <div>{label}</div>
</a>

<style>
  a:hover > .icon,
  .active > .icon {
    @apply bg-a-gray-100;
  }
</style>
