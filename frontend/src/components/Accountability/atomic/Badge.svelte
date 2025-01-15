<script lang="ts">
  import IconBookmark from "../icons/IconBookmark.svelte"
  import IconCheck from "../icons/IconCheck.svelte"
  import IconEye from "../icons/IconEye.svelte"
  import IconOpenExternal from "../icons/IconOpenExternal.svelte"
  import IconXMark from "../icons/IconXMark.svelte"

  interface Props {
    label?: string
    notification?: boolean
    href?: string
    button?: boolean
    disabled?: boolean
    size?: "base" | "small"
    icon?: "" | "check" | "eye" | "bookmark"
    iconRight?: boolean
    color?: "primary" | "warning" | "error" | "success" | "neutral" | "blue"
    variant?: "filled" | "light" | "filled-light"
    onclick?: () => void
  }

  let {
    label = "Badge",
    notification = false,
    href = "",
    button = false,
    disabled = false,
    size = "small",
    icon = "",
    iconRight = false,
    color = "primary",
    variant = "light",
    onclick,
  }: Props = $props()

  let iconSize = $derived(size === "base" ? "24" : "16")

  const icons = [
    { icon: "check", component: IconCheck },
    { icon: "eye", component: IconEye },
    { icon: "bookmark", component: IconBookmark },
    { icon: "link", component: IconOpenExternal },
  ]
</script>

{#if href}
  <a
    class:disabled
    class="wrapper cursor-pointer {size} {icon} {color} {variant} {disabled
      ? '!bg-a-gray-100 !text-a-gray-400'
      : ''} "
    {href}
    target="_blank"
  >
    <span class="line-clamp-1">{label}</span>
    <IconOpenExternal size={iconSize} />
  </a>
{:else}
  <div class:disabled class="wrapper {size} {icon} {color} {variant}">
    {#if icon && !iconRight}
      {@const IconComponent = icons.find(e => e.icon == icon)?.component}
      <IconComponent size={iconSize} />
    {/if}

    {#if notification}
      <div
        class="notification inline-block rounded-xl {disabled ? '!bg-a-gray-400' : ''} "
      ></div>
    {/if}

    <span class="line-clamp-1">{label}</span>

    <!-- {#if button && !link} -->
    {#if button}
      <button {disabled} {onclick}>
        <IconXMark size={iconSize} />
      </button>
    {/if}

    {#if icon && iconRight}
      {@const TrailingIconComponent = icons.find(e => e.icon == icon)?.component}
      <TrailingIconComponent size={iconSize} />
    {/if}
  </div>
{/if}

<style>
  .wrapper {
    @apply h-9 w-fit;
    @apply px-4;
    @apply flex items-center gap-1.5;
    @apply rounded;
    @apply text-a-base font-medium;
  }

  .wrapper > .notification {
    @apply h-3 w-3;
  }

  .wrapper.small {
    @apply h-[1.375rem];
    @apply px-2;
    @apply text-a-sm;
  }

  .wrapper.small .notification {
    @apply h-2 w-2;
  }

  /* Light color variants */
  .light.primary {
    @apply bg-a-primary-200 text-a-primary-500;
  }
  .light.primary > .notification {
    @apply bg-a-primary-500;
  }

  .light.warning {
    @apply bg-a-warning-100 text-a-warning-600;
  }
  .light.warning > .notification {
    @apply bg-a-warning-600;
  }

  .light.error {
    @apply bg-a-error-100 text-a-error-500;
  }
  .light.error > .notification {
    @apply bg-a-error-500;
  }

  .light.success {
    @apply bg-a-success-100 text-a-success-600;
  }
  .light.success > .notification {
    @apply bg-a-success-600;
  }

  .light.neutral {
    @apply bg-a-gray-100 text-a-gray-800;
  }
  .light.neutral > .notification {
    @apply bg-a-gray-800;
  }

  /* Filled color variants */
  .filled {
    @apply text-white;
  }
  .filled > .notification {
    @apply bg-white;
  }

  .filled.primary {
    @apply bg-a-primary-500;
  }
  .filled.warning {
    @apply bg-a-warning-500;
  }
  .filled.error {
    @apply bg-a-error-500;
  }
  .filled.success {
    @apply bg-a-success-500;
  }
  .filled.neutral {
    @apply bg-a-gray-800;
  }

  .blue {
    @apply bg-a-blue;
  }
</style>
