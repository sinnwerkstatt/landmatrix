<script lang="ts">
  interface Props {
    class?: string
  }

  let { class: className = "size-4" }: Props = $props()
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
    d="M15 12H9m12 0a9 9 0 11-18 0 9 9 0 0118 0z"
  />
</svg>
