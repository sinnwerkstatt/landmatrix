<script lang="ts">
  import type { SvelteComponent } from "svelte"

  interface Props {
    items?: { label: string; value: number; component: SvelteComponent }[]
  }

  let { items = [] }: Props = $props()
  let activeTabValue = $state(1);
  const handleClick = tabValue => () => (activeTabValue = tabValue)
</script>

<div class="flex h-full flex-col">
  <ul class="flex justify-center gap-1">
    {#each items as item}
      <li class={activeTabValue === item.value ? "active" : ""}>
        <button onclick={handleClick(item.value)}>{item.label}</button>
      </li>
    {/each}
  </ul>

  {#each items as item}
    {#if activeTabValue == item.value}
      <div class="flex h-full flex-col gap-2 overflow-x-auto overflow-y-hidden pt-2">
        <item.component />
      </div>
    {/if}
  {/each}
</div>

<style>
  button {
    @apply w-fit;
    @apply px-[0.63rem] py-[0.44rem];
    @apply text-a-sm text-a-gray-400;
    @apply rounded-lg border border-a-gray-200;
    @apply bg-white;
  }
  button:hover {
    @apply cursor-pointer;
    @apply bg-a-gray-200 text-a-gray-900;
  }
  li.active > button {
    @apply border-a-gray-900 bg-a-gray-900 text-white;
  }
</style>
