<script lang="ts">
  import ContextBarContainer from "../ContextBarContainer.svelte"
  import FilterBar from "../FilterBar.svelte"
  import { showContextBar, showFilterBar } from "../stores"
  import ViewSwitcher from "../ViewSwitcher.svelte"
</script>

<div class="relative h-full w-full p-0">
  <!--  <ViewSwitcher />-->
  <FilterBar />
  <ContextBarContainer>
    <slot name="ContextBar" />
  </ContextBarContainer>
  <div class="h-full w-full">
    <div class="float-left h-full w-0 xl:w-[clamp(220px,20%,300px)]" />
    <div class="float-right h-full w-0 xl:w-[clamp(220px,20%,300px)]" />
    <div class="h-full overflow-auto">
      <slot />
    </div>
  </div>
</div>
