<script lang="ts">
  import Avatar from "./Avatar.svelte"

  interface Props {
    users?: { id: number; name: string; initials: string }[]
    size?: "sm" | "md"
    maxAvatars?: number
  }

  let { users = [], size = "md", maxAvatars = 4 }: Props = $props()

  let box: HTMLElement = $state()
  let boxWidth: HTMLElement = $state()

  const dimensions = [
    { label: "sm", size: 24 },
    { label: "md", size: 32 },
  ]

  function getDimensions(size) {
    const ring = 6
    const dims = dimensions.find(e => e.label == size)
    const total = dims.size + ring - 4
    return total
  }

  function avatarsToDisplay(boxWidth, users, maxAvatars) {
    let result = {
      users: [],
      rest: 0,
    }

    if (!users && users.length < 1) return result

    if (maxAvatars == 0) {
      result.users = []
      result.rest = users.length
    }

    const avatarWidth = getDimensions(size)
    const slots = Math.floor(boxWidth / avatarWidth)
    const n = slots > maxAvatars ? maxAvatars : slots

    result.users = users.slice(0, n)
    result.rest = users.length - result.users.length

    return result
  }

  let avatars = $derived(avatarsToDisplay(boxWidth, users, maxAvatars))
</script>

<div class="relative {size} w-full" bind:this={box} bind:offsetWidth={boxWidth}>
  {#each avatars.users as { name, initials }}
    <span class="avatar">
      <Avatar {name} {initials} {size} ring={true} />
    </span>
  {/each}

  {#if avatars?.rest > 0}
    <span class="avatar">
      <Avatar tooltip={false} initials="+{avatars?.rest}" {size} ring={true} />
    </span>
  {/if}
</div>

<style>
  .sm,
  .md {
    @apply pl-1;
  }

  .sm .avatar,
  .md .avatar {
    @apply relative -ml-1 inline-block;
  }
</style>
