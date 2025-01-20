<script lang="ts">
  import IconBookmark from "../icons/IconBookmark.svelte"
  import IconCheck from "../icons/IconCheck.svelte"
  import IconEye from "../icons/IconEye.svelte"
  import IconTrashcan from "../icons/IconTrashcan.svelte"

  interface Props {
    icon?: string
    color?: string // Directly add Tailwind style
    children?: import("svelte").Snippet
    onclick?: () => void
  }

  let { icon = "check", color = "", children, onclick }: Props = $props()

  const icons = [
    { icon: "check", component: IconCheck },
    { icon: "eye", component: IconEye },
    { icon: "bookmark", component: IconBookmark },
    { icon: "trashcan", component: IconTrashcan },
  ]

  const SvelteComponent = $derived(icons.find(e => e.icon == icon)?.component)
</script>

<button
  {onclick}
  class="flex items-center gap-3 bg-white px-4 py-2 hover:bg-a-gray-100"
>
  <span class={color}>
    <SvelteComponent size={18} />
  </span>
  {@render children?.()}
</button>
