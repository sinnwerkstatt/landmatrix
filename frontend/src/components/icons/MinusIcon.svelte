<script lang="ts">
  interface Props {
    class?: string
  }

  let { class: className = "inline size-4" }: Props = $props()
</script>

<svg
  role="none"
  xmlns="http://www.w3.org/2000/svg"
  class={className}
  fill="none"
  viewBox="0 0 24 24"
  stroke="currentColor"
  stroke-width="2"
>
  <path stroke-linecap="round" stroke-linejoin="round" d="M20 12H4" />
</svg>
