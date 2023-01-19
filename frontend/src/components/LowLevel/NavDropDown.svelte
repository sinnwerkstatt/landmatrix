<script lang="ts">
  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"

  export let title = ""
  export let placement = ""
</script>

<li class="group relative {$$props.class}">
  <div class="flex cursor-default items-center gap-2 p-2 hover:text-orange">
    {#if title}
      {title}
      <ChevronDownIcon />
    {:else}
      <slot name="title" />
    {/if}
  </div>
  <div class="absolute hidden group-hover:block group-focus:block {placement}">
    <slot />
  </div>
</li>
