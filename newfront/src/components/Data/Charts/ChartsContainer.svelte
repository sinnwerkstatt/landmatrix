<script lang="ts">
  import ContextBarContainer from "../ContextBarContainer.svelte"
  import FilterBar from "../FilterBar.svelte"
  import { showContextBar, showFilterBar } from "../index"
  import ViewSwitcher from "../ViewSwitcher.svelte"
</script>

<div class="relative h-full w-full p-0">
  <ViewSwitcher />
  <FilterBar />
  <ContextBarContainer>
    <slot name="ContextBar" />
  </ContextBarContainer>
  <div class="h-full w-full">
    <div
      class="{$showFilterBar ? 'w-[clamp(220px,20%,300px)]' : 'w-0'} float-left h-full"
    />
    <div
      class="{$showContextBar
        ? 'w-[clamp(220px,20%,300px)]'
        : 'w-0'} float-right h-full"
    />
    <div class="flex h-full justify-center overflow-x-auto overflow-y-auto text-center">
      <slot />
    </div>
  </div>
</div>
