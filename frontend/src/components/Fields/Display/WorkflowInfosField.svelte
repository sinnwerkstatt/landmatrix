<script lang="ts">
  import { slide } from "svelte/transition"

  import type { WorkflowInfo as WFInfo } from "$lib/types/generics"

  import type { FormField } from "$components/Fields/fields"
  import WorkflowInfo from "$components/Management/WorkflowInfo.svelte"

  export let value: WFInfo[]
  export let formfield: FormField

  let showMoreInfos = false

  function clickOutside(element, callbackFunction) {
    function onClick(event) {
      if (!element.contains(event.target)) callbackFunction()
    }

    document.body.addEventListener("click", onClick)

    // the destroy function is actually in use, linter is wrong
    // noinspection JSUnusedGlobalSymbols
    return {
      update(newCallbackFunction) {
        callbackFunction = newCallbackFunction
      },
      destroy() {
        document.body.removeEventListener("click", onClick)
      },
    }
  }
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
      use:clickOutside={() => (showMoreInfos = !showMoreInfos)}
      class="absolute top-0 z-10 w-[368px] rounded-sm border border-black bg-lm-warmgray shadow-md"
    >
      <div
        class="h-auto max-h-[330px] cursor-default overflow-y-scroll bg-lm-warmgray px-[2px] pt-1 pb-4 shadow-inner"
      >
        {#each value as info}
          <WorkflowInfo bind:info />
        {/each}
      </div>
    </div>
  {/if}
</div>
