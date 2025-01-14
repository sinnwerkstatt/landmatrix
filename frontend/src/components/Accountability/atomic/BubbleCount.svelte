<script lang="ts">
  interface Props {
    size?: string // base, sm, lg
    count?: number // Any number
  }

  let { size = "base", count = 0 }: Props = $props()
</script>

<span class="bubble {size}">
  {#if count > 99}
    <span class="smaller">99+</span>
  {:else}
    <span>{count}</span>
  {/if}
</span>

<style>
  .bubble {
    @apply h-4 w-4;
    @apply flex place-content-center pt-0.5;
    @apply text-a-xs text-white;
    @apply rounded-full bg-a-primary-500;
    @apply ring-[1.5px] ring-white;
  }

  .bubble.sm {
    @apply h-2 w-2;
  }
  .bubble.sm > span {
    @apply hidden;
  }

  .bubble.lg {
    @apply h-6 w-6;
    @apply text-a-sm;
  }

  .smaller {
    @apply text-[0.5rem];
  }

  .lg .smaller {
    @apply pt-1 text-a-xs;
  }
</style>
