<script lang="ts">
  import { page } from "$app/stores"

  export let label = "Item"
  export let href = "/accountability/"
</script>

<a
  {href}
  class:active={$page.url.pathname.startsWith(href)}
  class="flex flex-col items-center gap-1 text-a-s font-semibold text-a-gray-900 hover:text-a-gray-900"
>
  <span class="icon rounded-lg p-2">
    <slot name="icon" />
  </span>
  <div>{label}</div>
</a>

<style>
  a:hover > .icon,
  .active > .icon {
    @apply bg-a-gray-100;
  }
</style>
