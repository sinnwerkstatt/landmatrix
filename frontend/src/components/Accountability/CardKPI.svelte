<script lang="ts">
  import Card from "./atomic/Card.svelte"
  import Loader from "./atomic/Loader.svelte"
  import Button from "./Button.svelte"
  import IconCheckCircle from "./icons/IconCheckCircle.svelte"
  import IconEye from "./icons/IconEye.svelte"

  interface Props {
    label?: string
    value?: string
    button?: string
    href?: string
    hrefLabel?: string
    loader?: boolean
    color?: "neutral" | "orange" | "green"
    icon?: "" | "check" | "eye"
    labelPosition?: "top" | "bottom"
    onclick?: () => void
  }

  let {
    label = "Label",
    value = "Value",
    button = "",
    href = "",
    hrefLabel = "A link leading to href",
    loader = false,
    color = "neutral",
    icon = "",
    labelPosition = "bottom",
    onclick,
  }: Props = $props()

  const icons = [
    { icon: "", component: false },
    { icon: "check", component: IconCheckCircle },
    { icon: "eye", component: IconEye },
  ]

  let colorScheme = $derived.by(() => {
    if (color == "orange") return "bg-a-primary-100 text-a-primary-500"
    if (color == "green") return "bg-a-success-50 text-a-success-500"
    return "bg-a-gray-100 text-a-gray-900"
  })
</script>

<Card>
  <div class="flex flex-col gap-4">
    {#if labelPosition == "top"}
      <span class="label">{label}</span>
    {/if}

    <div class="flex items-center gap-2">
      {#if icon}
        {@const SvelteComponent = icons.find(e => e.icon == icon)?.component}
        <div class="grid h-[3rem] w-[3rem] place-items-center rounded-lg {colorScheme}">
          <SvelteComponent size="24" />
        </div>
      {/if}
      {#if loader}
        <Loader />
      {:else}
        <span class="text-a-2xl font-semibold">{value}</span>
      {/if}
    </div>

    <div class="flex items-center justify-between gap-2">
      {#if labelPosition != "top"}
        <span class="label">{label}</span>
      {/if}

      {#if button}
        <Button type="outline" style="neutral" label={button} {onclick} />
      {/if}

      {#if href}
        <a class="link" {href}>{hrefLabel}</a>
      {/if}
    </div>
  </div>
</Card>

<style>
  .label {
    @apply text-a-sm font-normal text-a-gray-500;
  }
</style>
