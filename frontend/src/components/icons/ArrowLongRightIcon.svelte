<script lang="ts">
  interface Props {
    class?: string
  }

  let { class: className = "inline size-4" }: Props = $props()
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  fill="none"
  viewBox="0 0 24 24"
  stroke-width="1.5"
  stroke="currentColor"
  class={className}
>
  <path
    stroke-linecap="round"
    stroke-linejoin="round"
    d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3"
  />
</svg>
