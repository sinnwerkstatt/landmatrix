<script lang="ts">
  interface Props {
    class?: string
  }

  let { class: className = "inline size-4" }: Props = $props()
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  class={className}
  viewBox="0 0 72 96"
  fill="currentColor"
>
  <path
    d="M32.3003 94.0631C5.05688 54.5683 0 50.5149 0 36C0 16.1177 16.1177 0 36 0C55.8823 0 72 16.1177 72 36C72 50.5149 66.9431 54.5683 39.6997 94.0631C37.9119 96.6458 34.0879 96.6456 32.3003 94.0631ZM36 51C44.2843 51 51 44.2843 51 36C51 27.7157 44.2843 21 36 21C27.7157 21 21 27.7157 21 36C21 44.2843 27.7157 51 36 51Z"
  />
</svg>
