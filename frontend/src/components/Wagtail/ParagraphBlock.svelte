<script lang="ts">
  export let value: string
</script>

<div data-block="paragraph" class="paragraph mb-6 break-words" data-sveltekit-reload>
  {@html value}
</div>

<style lang="postcss">
  :global(.paragraph ol) {
    @apply list-decimal pl-4;
  }
  :global(.paragraph ul) {
    @apply mb-4 list-disc pl-4;
  }
  :global(.paragraph h2) {
    @apply heading3 mb-3;
  }
  :global(.paragraph h3) {
    @apply heading4 mb-2;
  }
  :global(.paragraph h4) {
    @apply heading5 mb-2;
  }
  :global(.paragraph p) {
    @apply mb-4;
  }
  :global(.paragraph a) {
    @apply text-orange transition hover:text-orange-700;
  }
</style>
