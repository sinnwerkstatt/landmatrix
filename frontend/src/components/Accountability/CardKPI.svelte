<script lang="ts">
  import Card from "./atomic/Card.svelte"
  import Loader from "./atomic/Loader.svelte"
  import Button from "./Button.svelte"
  import IconCheckCircle from "./icons/IconCheckCircle.svelte"
  import IconEye from "./icons/IconEye.svelte"

  export let label: string = "Label"
  export let value: string = "Value"
  export let button: string = ""
  export let href: string = ""
  export let hrefLabel = "A link leading to href"
  export let loader = false

  export let color: "neutral" | "orange" | "green" = "neutral"
  export let icon: "" | "check" | "eye" = ""
  export let labelPosition: "top" | "bottom" = "bottom"

  const icons = [
    { icon: "", component: false },
    { icon: "check", component: IconCheckCircle },
    { icon: "eye", component: IconEye },
  ]

  function getColorScheme() {
    if (color == "orange") return "bg-a-primary-100 text-a-primary-500"
    if (color == "green") return "bg-a-success-50 text-a-success-500"
    return "bg-a-gray-100 text-a-gray-900"
  }

  $: colorScheme = getColorScheme()
</script>

<Card>
  <div class="flex flex-col gap-4">
    {#if labelPosition == "top"}
      <span class="label">{label}</span>
    {/if}

    <div class="flex items-center gap-2">
      {#if icon}
        <div class="grid h-[3rem] w-[3rem] place-items-center rounded-lg {colorScheme}">
          <svelte:component
            this={icons.find(e => e.icon == icon)?.component}
            size="24"
          />
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
        <Button type="outline" style="neutral" label={button} on:click />
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
