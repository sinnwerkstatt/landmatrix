<script lang="ts">
    import { page } from "$app/stores"
    import { users } from "$lib/accountability/placeholders"
    import { deals } from "$lib/accountability/placeholders"

    import TableVariables from "$components/Accountability/TableVariables.svelte"
    import DrawerScoring from "$components/Accountability/DrawerScoring.svelte"

    import Badge from "$components/Accountability/atomic/Badge.svelte"
    import IconChevron from "$components/Accountability/icons/IconChevron.svelte"
    import AvatarGroup from "$components/Accountability/atomic/AvatarGroup.svelte"

    const href = $page.url.href.substring(0, $page.url.href.indexOf("scoring/") + "scoring/".length);
</script>

<div class="h-full w-full flex flex-col px-4 py-6">
    <div class="flex items-center gap-2">
        <a class="-rotate-90 text-a-gray-900 hover:text-a-gray-900" {href} >
            <IconChevron />
        </a>
        <span class="text-a-2xl font-semibold">Deal #{$page.params.deal}</span>
        <Badge color="neutral" variant="light" />
    </div>

    <div class="mt-2 mb-6">
        <AvatarGroup users={users} maxAvatars=4 />
    </div>
    
    <div class="h-full">
        <TableVariables deal={deals[0]} />
    </div>
</div>
