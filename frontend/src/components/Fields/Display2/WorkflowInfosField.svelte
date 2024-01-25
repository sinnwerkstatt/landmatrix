<script lang="ts">
  import { slide } from "svelte/transition"

  import { clickOutside } from "$lib/helpers"
  import type { WorkflowInfoType } from "$lib/types/newtypes"

  import WorkflowInfoNew from "$components/New/WorkflowInfoNew.svelte"

  export let value: WorkflowInfoType[]

  let showMoreInfos = false
</script>

<!--{JSON.stringify(value)}-->
<div
  class="cursor-pointer"
  on:click|stopPropagation={() => {
    if (!showMoreInfos) showMoreInfos = true
  }}
>
  <slot>
    <WorkflowInfoNew isDeal info={value[0]} />
  </slot>
  <!--{#if showMoreInfos}-->
  <!--  <div-->
  <!--    transition:slide-->
  <!--    use:clickOutside-->
  <!--    on:outClick={() => (showMoreInfos = false)}-->
  <!--    class="bg-lm-darkgray absolute top-0 z-10 w-[368px] rounded-sm border border-black shadow-md"-->
  <!--  >-->
  <!--    <div-->
  <!--      class="bg-lm-darkgray h-auto max-h-[330px] cursor-default overflow-y-scroll px-[2px] pb-4 pt-1 shadow-inner"-->
  <!--    >-->
  <!--      {#each value as info}-->
  <!--        <WorkflowInfoNew bind:info />-->
  <!--      {/each}-->
  <!--    </div>-->
  <!--  </div>-->
  <!--{/if}-->
</div>
