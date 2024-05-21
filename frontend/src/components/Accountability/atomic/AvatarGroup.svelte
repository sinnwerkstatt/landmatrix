<script lang="ts">
    import Avatar from "./Avatar.svelte"

    export let users:{id:number, name:string, initials:string}[] = []
    export let size:"sm"|"md" = "md"
    export let maxAvatars = 4

    let box:HTMLElement
    let boxWidth:HTMLElement

    const dimensions = [
        { label: "sm", size: 24 },
        { label: "md", size: 32 }
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
            rest: 0
        }

        if (!users && users.length < 1) return result

        if(maxAvatars == 0) {
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

    $: avatars = avatarsToDisplay(boxWidth, users, maxAvatars)

</script>

<div class="relative {size} w-full" bind:this={box} bind:offsetWidth={boxWidth} >
    {#each avatars.users as { id, name, initials }}
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
        @apply inline-block relative -ml-1;
    }
</style>