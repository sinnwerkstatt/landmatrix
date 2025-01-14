<script lang="ts">
  import BubbleCount from "$components/Accountability/atomic/BubbleCount.svelte"


  interface Props {
    label?: string;
    type?: "fill" | "outline" | "ghost";
    style?: "primary" | "neutral" | "error";
    size?: "base" | "sm" | "lg";
    count?: number;
    tailwind?: string; // additional tailwind classes
    disabled?: boolean;
    iconAfter?: import('svelte').Snippet;
    onclick?: () => void
  }

  let {
    label = "Label",
    type = "fill",
    style = "primary",
    size = "base",
    count = 0,
    tailwind = "",
    disabled = false,
    iconAfter,
    onclick
  }: Props = $props();
</script>

<button class="{style} {size} {type} {tailwind}" {disabled} {onclick}>
  <span class="flex items-center gap-3">
    {label}
    {@render iconAfter?.()}
  </span>
  {#if count > 0}
    <span class="bubble">
      <BubbleCount {count} {size} />
    </span>
  {/if}
</button>

<style>
  button {
    @apply w-fit;
    @apply flex justify-center;
    @apply font-medium text-white;
    @apply rounded-lg;
    @apply relative;
  }
  button.outline,
  button.ghost {
    @apply bg-transparent;
  }
  button.outline {
    @apply outline-[1.5px] outline-offset-[-1.5px];
  }
  button:active:enabled {
    @apply ring-4;
  }
  button:disabled {
    @apply bg-a-gray-300;
  }
  button.outline:disabled,
  button.ghost:disabled {
    @apply bg-transparent text-a-gray-300 outline-a-gray-300;
  }

  /* Sizes */
  .sm {
    @apply px-3 py-1.5;
    @apply text-a-s;
  }

  .base {
    @apply px-4 py-2;
    @apply text-a-sm;
  }

  .lg {
    @apply px-5.5 py-2.5;
    @apply text-a-base;
  }

  /* Primary */
  .primary {
    @apply bg-a-primary-500;
  }
  .primary:hover:enabled {
    @apply bg-a-primary-600;
  }
  .primary.outline,
  .primary.ghost {
    @apply text-a-primary-500;
  }
  .primary.outline:hover:enabled,
  .primary.ghost:hover:enabled {
    @apply bg-a-primary-100;
  }
  .primary:active {
    @apply ring-a-lavender;
  }

  /* Neutral */
  .neutral {
    @apply bg-a-gray-900;
  }
  .neutral:hover:enabled {
    @apply bg-a-gray-800;
  }
  .neutral.outline,
  .neutral.ghost {
    @apply text-a-gray-900 outline-a-gray-300;
  }
  .neutral.outline:hover:enabled,
  .neutral.ghost:hover:enabled {
    @apply bg-a-gray-100;
  }
  .neutral:active {
    @apply ring-a-gray-ring;
  }

  /* Error */
  .error {
    @apply bg-a-error-500;
  }
  .error:hover:enabled {
    @apply bg-a-error-600;
  }
  .error.outline,
  .error.ghost {
    @apply text-a-error-500;
  }
  .error.outline:hover:enabled,
  .error.ghost:hover:enabled {
    @apply bg-a-error-50;
  }
  .error:active {
    @apply ring-a-error-200;
  }

  /* Bubble count */
  .bubble {
    @apply absolute;
    @apply -right-1 -top-1;
  }
  .sm > .bubble {
    @apply -right-0.5 -top-0.5;
  }
  .lg > .bubble {
    @apply -right-2 -top-2;
  }
</style>
