<script lang="ts">
  import { page } from "$app/state"

  import { users } from "$lib/accountability/placeholders"
  import { deals } from "$lib/accountability/stores"

  import AvatarGroup from "$components/Accountability/atomic/AvatarGroup.svelte"
  import Badge from "$components/Accountability/atomic/Badge.svelte"
  import IconChevron from "$components/Accountability/icons/IconChevron.svelte"
  import TableVariables from "$components/Accountability/TableVariables.svelte"

  const href = page.url.href.substring(
    0,
    page.url.href.indexOf("scoring/") + "scoring/".length,
  )

  // $: console.log($deals)
</script>

<div class="flex h-full w-full flex-col px-4 py-6">
  <div class="flex items-center gap-2">
    <a class="-rotate-90 text-a-gray-900 hover:text-a-gray-900" {href}>
      <IconChevron />
    </a>
    <span class="text-a-2xl font-semibold">Deal #{page.params.deal}</span>
    <Badge color="neutral" variant="light" />
  </div>

  <div class="mb-6 mt-2">
    <AvatarGroup {users} maxAvatars={4} />
  </div>

  <div class="h-full">
    <TableVariables deal={$deals[0]} />
  </div>
</div>
