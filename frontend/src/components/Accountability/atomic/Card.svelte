<script lang="ts">
  interface Props {
    extraClass?: string
    children?: import("svelte").Snippet
  }

  let { extraClass = "", children }: Props = $props()
</script>

<div class="rounded-lg border border-a-gray-200 bg-white p-4 {extraClass}">
  {@render children?.()}
</div>
