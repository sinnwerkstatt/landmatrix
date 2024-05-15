<script lang="ts">
    import dayjs from "dayjs"
    import relativeTime from 'dayjs/plugin/relativeTime'

    import { capitalizeFirst } from "$lib/accountability/helpers"

    import Avatar from "./Avatar.svelte"
    import Embed from "./Embed.svelte"
    import Badge from "./Badge.svelte"

    export let data:{ user:{name:string, initials:string}, 
                      type:string, deal:number, 
                      timestamp:string } = {
        user: { name: "Placeholder", initials: "P" },
        type: "score",
        score: "undefined",
        timestamp: "2024-05-12T14:48:00.000+09:00"
    }

    export let line = false

    function getColorPalette(score) {
        if (score == "validated") return "success"
        return "primary"
    }

    function getRelativeTime() {
        dayjs.extend(relativeTime)
        return dayjs(data.timestamp).fromNow()
    }

    $: time = getRelativeTime()

</script>

<div class="wrapper">
    <div class="flex flex-col items-center">
        <Avatar initials={data.user.initials} />

        {#if line}
            <div class="bg-a-gray-200 w-[0.06rem] h-full"></div>
        {/if}

    </div>

    <div class="text-a-sm pb-6">
        <div class="flex items-center gap-1">
            <span>{data.user.name}</span>

            {#if data.type == "score"}
                <span class="sentence">set</span>
                <Embed label="V{data.variable}" />
                <span class="sentence">in</span>
                <Embed label="#{data.deal}" />
                <span class="sentence">to</span>
                <Badge label={capitalizeFirst(data.score)} color={getColorPalette(data.score)} />
            {/if}
        </div>
        
        <span class="sentence">{time}</span>

        {#if data.comment}
            <div class="mt-1 p-4 rounded-lg border boder-a-gray-100 font-normal bg-white">
                {data.comment}
            </div>
        {/if}

    </div>
</div>

<style>
    .wrapper {
        @apply grid gap-2;
        grid-template-columns: 2rem auto;
    }
    .sentence {
        @apply font-normal text-a-gray-500;
    }
</style>