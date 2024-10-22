<script lang="ts">
  export let label = ""
</script>

{#if label}
  <div class="flex h-8 flex-row items-center gap-1 text-a-gray-400">
    <span class="hr"></span>
    <span class="text-a-s">{label}</span>
    <span class="hr"></span>
  </div>
{:else}
  <hr class="my-4" />
{/if}

<style>
  .hr {
    @apply grow;
    @apply h-[1px];
    @apply bg-a-gray-200;
  }
</style>
