<script lang="ts">
  interface Props {
    style?: "base" | "heading" | "nested"
    children?: import("svelte").Snippet
  }

  let { style = "base", children }: Props = $props()
</script>

<div class={style}>{@render children?.()}</div>

<style>
  div {
    @apply h-14 w-full;
    @apply px-2 py-4;
    @apply overflow-hidden;
    @apply grid items-center;
    @apply bg-white;
  }

  div.heading,
  div.nested {
    @apply p-2;
    @apply bg-a-gray-50;
  }

  div.heading {
    @apply h-8;
    @apply text-a-gray-500;
  }

  div.nested {
    @apply h-10;
  }
</style>
