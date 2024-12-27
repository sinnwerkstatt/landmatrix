<script lang="ts">
  import type { Snippet } from "svelte"

  import ContextBarContainer from "../ContextBarContainer.svelte"
  import FilterBar from "../FilterBar.svelte"
  import ViewSwitcher from "../ViewSwitcher.svelte"

  interface Props {
    ContextBar?: Snippet
    children?: Snippet
  }

  let { ContextBar, children }: Props = $props()
</script>

<div class="relative h-full w-full p-0">
  <ViewSwitcher />
  <FilterBar />
  <ContextBarContainer>
    {@render ContextBar?.()}
  </ContextBarContainer>
  <div class="h-full w-full">
    <div class="float-left h-full w-0 xl:w-[clamp(220px,20%,300px)]"></div>
    <div class="float-right h-full w-0 xl:w-[clamp(220px,20%,300px)]"></div>
    <div class="flex h-full flex-col overflow-auto text-center md:flex-row">
      <div class="mt-16 flex-grow md:mx-4 md:px-5">
        {@render children?.()}
      </div>
    </div>
  </div>
</div>
