<script lang="ts">
  import type { Snippet } from "svelte"

  import ContextBarMap from "./ContextBarMap.svelte"
  import FilterBar from "./FilterBar.svelte"
  import ViewSwitcher from "./ViewSwitcher.svelte"

  interface Props {
    FilterBarSnippet?: Snippet
    children: Snippet
  }
  let { FilterBarSnippet, children }: Props = $props()
</script>

<div class="relative h-full w-full p-0">
  <ViewSwitcher />
  <FilterBar>
    {@render FilterBarSnippet?.()}
  </FilterBar>
  <ContextBarMap />
  <div class="h-full w-full">
    {@render children()}
  </div>
</div>
