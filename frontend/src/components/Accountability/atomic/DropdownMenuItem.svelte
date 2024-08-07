<script lang="ts">
    import IconEye from "../icons/IconEye.svelte"
    import IconCheck from "../icons/IconCheck.svelte"
    import IconBookmark from "../icons/IconBookmark.svelte"
    import IconTrashcan from "../icons/IconTrashcan.svelte"

    export let icon = "check"
    export let color = "" // Directly add Tailwind style

    const icons = [
        { icon: "check", component: IconCheck },
        { icon: "eye", component: IconEye },
        { icon: "bookmark", component: IconBookmark },
        { icon: "trashcan", component: IconTrashcan },
    ]
</script>

<button on:click class="flex items-center px-4 py-2 gap-3 bg-white hover:bg-a-gray-100">
    <span class="{color}">
        <svelte:component this={icons.find(e => e.icon == icon)?.component} size={18} />
    </span>
    <slot />
</button>