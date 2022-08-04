<script lang="ts">
  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte";

  export let title = "";
  export let placement = "";
</script>

<li class="group relative {$$props.class}">
  <div class="flex items-center cursor-default gap-2 hover:text-orange p-2">
    {#if title}
      {title}
      <ChevronDownIcon />
    {:else}
      <slot name="title" />
    {/if}
  </div>
  <div class="hidden absolute group-hover:block group-focus:block {placement}">
    <slot />
  </div>
</li>
