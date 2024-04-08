<script lang="ts">
    import { page } from "$app/stores"

    export let label = "Item"
    export let href = "/accountability/"
</script>

<a {href} class:active={$page.url.pathname.startsWith(href)}
   class="flex flex-col gap-1 items-center text-a-s text-a-gray-900 hover:text-a-gray-900">
    <span class="icon p-2 rounded-lg">
        <slot name="icon" />
    </span>
    <div>{label}</div>
</a>

<style>
    a:hover > .icon,
    .active > .icon {
        @apply bg-a-gray-100;
    }
</style>