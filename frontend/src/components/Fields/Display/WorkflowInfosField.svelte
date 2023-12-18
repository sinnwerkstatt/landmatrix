<script lang="ts">
  import { slide } from "svelte/transition"

  import { clickOutside } from "$lib/helpers"
  import type { WorkflowInfo as WFInfo } from "$lib/types/generics"

  import type { FormField } from "$components/Fields/fields"
  import WorkflowInfo from "$components/Management/WorkflowInfo.svelte"

  export let value: WFInfo[]
  export let formfield: FormField

  let showMoreInfos = false
</script>

<div
  class="cursor-pointer"
  on:click|stopPropagation={() => {
    if (!showMoreInfos) showMoreInfos = true
  }}
>
  <slot>
    <WorkflowInfo bind:info={value[0]} />
  </slot>
  {#if showMoreInfos}
    <div
      transition:slide
      use:clickOutside
      on:outClick={() => (showMoreInfos = false)}
      class="absolute top-0 z-10 w-[368px] rounded-sm border border-black bg-gray-100 shadow-md"
    >
      <div
        class="h-auto max-h-[330px] cursor-default overflow-y-scroll bg-gray-100 px-[2px] pb-4 pt-1 shadow-inner"
      >
        {#each value as info}
          <WorkflowInfo bind:info />
        {/each}
      </div>
    </div>
  {/if}
</div>
