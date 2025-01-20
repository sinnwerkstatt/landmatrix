<script lang="ts">
  interface Props {
    class?: string
  }

  let { class: className = "inline size-4" }: Props = $props()
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  class={className}
  viewBox="0 0 30 30"
  fill="currentColor"
>
  <path
    d="M4 7h22M4 15h22M4 23h22"
    stroke="currentColor"
    stroke-linecap="round"
    stroke-miterlimit="10"
    stroke-width="2"
  />
</svg>
