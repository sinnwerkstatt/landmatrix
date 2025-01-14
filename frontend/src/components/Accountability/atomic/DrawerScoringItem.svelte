<script lang="ts">
  interface Props {
    label?: string
    description?: string
    value?: string
    score?: string
    onClick?: (value:string) => void
  }

  let {
    label = "Label",
    description = "Description",
    value = "NO_SCORE",
    score = "NO_SCORE",
    onClick,
  }: Props = $props()

  const colors = [
    { value: "NO_SCORE", class: "neutral" },
    { value: "NO_DATA", class: "black" },
    { value: "SEVERE_VIOLATIONS", class: "red" },
    { value: "PARTIAL_VIOLATIONS", class: "yellow" },
    { value: "NO_VIOLATIONS", class: "green" },
  ]

  let color = $derived(colors.find(e => e.value == value)?.class)

  function getBehavior(value, score) {
    if (score == "NO_SCORE") return ""
    if (value == score) return "active"
    return "dimmed"
  }

  let behavior = $derived(getBehavior(value, score))

</script>

<button
  class="min-w-40 grow rounded-lg border p-4 transition-colors {color} {behavior}"
  onclick={() => onClick?.(value)}
>
  <h2 class="mb-2 text-left text-a-base font-medium">{label}</h2>
  <p class="m-0 text-left text-a-sm font-normal text-a-gray-500">{description}</p>
</button>

<style>
  .black {
    @apply border-a-gray-900 bg-a-gray-50;
  }
  .black:hover,
  .black.active {
    @apply bg-a-gray-100;
  }

  .red {
    @apply border-a-error-500 bg-a-error-50;
  }
  .red:hover,
  .red.active {
    @apply bg-a-error-100;
  }

  .yellow {
    @apply border-a-warning-500 bg-a-warning-50;
  }
  .yellow:hover,
  .yellow.active {
    @apply bg-a-warning-100;
  }

  .green {
    @apply border-a-success-700 bg-a-success-50;
  }
  .green:hover,
  .green.active {
    @apply bg-a-success-100;
  }

  .dimmed {
    @apply border-a-gray-200 bg-white;
  }
  .dimmed:hover {
    @apply bg-a-gray-50;
  }
</style>
