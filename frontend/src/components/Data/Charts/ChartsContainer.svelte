<script lang="ts">
  import ContextBarContainer from "../ContextBarContainer.svelte"
  import FilterBar from "../FilterBar.svelte"
  import ViewSwitcher from "../ViewSwitcher.svelte"
</script>

<div class="relative h-full w-full p-0">
  <ViewSwitcher />
  <FilterBar />
  <ContextBarContainer>
    <slot name="ContextBar" />
  </ContextBarContainer>
  <div class="h-full w-full">
    <div class="float-left h-full w-0 xl:w-[clamp(220px,20%,300px)]" />
    <div class="float-right h-full w-0 xl:w-[clamp(220px,20%,300px)]" />
    <div class="flex h-full flex-col overflow-auto text-center md:flex-row">
      <div class="mx-4 mt-5 flex-grow">
        <slot />
      </div>
    </div>
  </div>
</div>
