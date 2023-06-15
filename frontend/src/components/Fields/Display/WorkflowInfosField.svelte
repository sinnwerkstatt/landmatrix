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
  class="workflowinfo-field cursor-pointer"
  data-name={formfield?.name ?? ""}
  on:click={event => {
    if (!showMoreInfos) showMoreInfos = true
    event.stopPropagation()
  }}
>
  <slot>
    <WorkflowInfo bind:info={value[0]} />
  </slot>
  {#if showMoreInfos}
    <div
      transition:slide
      use:clickOutside
      on:outClick={() => (showMoreInfos = !showMoreInfos)}
      class="absolute top-0 z-10 w-[368px] rounded-sm border border-black bg-lm-darkgray shadow-md"
    >
      <div
        class="h-auto max-h-[330px] cursor-default overflow-y-scroll bg-lm-darkgray px-[2px] pt-1 pb-4 shadow-inner"
      >
        {#each value as info}
          <WorkflowInfo bind:info />
        {/each}
      </div>
    </div>
  {/if}
</div>
