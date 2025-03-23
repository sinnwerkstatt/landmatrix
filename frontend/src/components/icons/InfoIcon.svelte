<script lang="ts">
  interface Props {
    class?: string
  }

  let { class: className = "inline size-6" }: Props = $props()
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  class={className}
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="1.4"
  stroke-linecap="round"
  stroke-linejoin="round"
  role="img"
  aria-label="Information icon"
>
  <circle cx="12" cy="12" r="10" />
  <line x1="12" y1="17" x2="12" y2="12" />
  <circle cx="12" cy="8" r="0.8" />
</svg>
