<script lang="ts">
  interface Props {
    class?: string
  }

  let { class: className = "inline size-4 rounded" }: Props = $props()
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  class={className}
  fill="none"
  viewBox="0 0 512 512"
>
  <path
    fill="currentColor"
    d="M222.7 32.15c5 16.93-4.6 34.75-21.6 39.79C121.8 95.55 64 169.1 64 255.1c0 106.9 85.1 192 192 192 106 0 192-85.1 192-192 0-86-57.8-159.55-137.1-183.16-17-5.04-26.6-22.86-21.6-39.79 5.1-16.94 22.9-26.588 39.8-21.55C434.9 42.07 512 139.1 512 255.1c0 142.3-114.6 256-256 256S0 397.4 0 255.1c0-116 77.15-213.03 182.9-244.5 16.9-5.038 34.7 4.61 39.8 21.55z"
  />
</svg>
