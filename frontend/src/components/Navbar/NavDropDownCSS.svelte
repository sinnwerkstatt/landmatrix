<script lang="ts">
  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"

  export let placement = "right-0"
</script>

<div class="group relative {$$props.class}">
  <button class="flex h-full items-center whitespace-nowrap p-2">
    <slot name="title" />

    <ChevronDownIcon
      class={"ml-0.5 h-4 w-4 transition duration-300 group-hover:rotate-180"}
    />
  </button>
  <div class="absolute z-50 hidden group-hover:block {placement}">
    <slot />
  </div>
</div>
