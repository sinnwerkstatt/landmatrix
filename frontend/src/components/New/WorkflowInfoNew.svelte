<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import dayjs from "dayjs"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { invalidate } from "$app/navigation"
  import { page } from "$app/stores"

  import { allUsers } from "$lib/stores"
  import { loading } from "$lib/stores.js"
  import type { WorkflowInfoType } from "$lib/types/newtypes"
  import { getCsrfToken } from "$lib/utils"

  import ArrowLongRightIcon from "$components/icons/ArrowLongRightIcon.svelte"
  import ChatBubbleLeftIcon from "$components/icons/ChatBubbleLeftIcon.svelte"
  import CheckCircleIcon from "$components/icons/CheckCircleIcon.svelte"

  export let info: WorkflowInfoType
  export let isDeal: boolean

  $: confidentialStatusChange = info.comment?.startsWith("[SET_CONFIDENTIAL]")
    ? "bg-red-400"
    : info.comment?.startsWith("[UNSET_CONFIDENTIAL]")
      ? "bg-green-600 line-through"
      : false

  $: cleanedComment = info.comment
    ?.replace("[SET_CONFIDENTIAL]", "")
    .replace("[UNSET_CONFIDENTIAL] ", "")

  $: openThread =
    info.status_after === info.status_before &&
    info.to_user_id &&
    [info.to_user_id, info.from_user_id].includes($page.data.user.id) &&
    !info.resolved

  let reply = ""

  async function sendReply() {
    loading.set(true)

    const ret = await fetch(
      `/api/workflow_info/${isDeal ? "deal" : "investor"}/${info.id}/add_reply/`,
      {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({ comment: reply }),
        headers: {
          "X-CSRFToken": await getCsrfToken(),
          "Content-Type": "application/json",
        },
      },
    )
    const retJson = await ret.json()
    if (!ret.ok || !retJson.ok) {
      toast.push(`Unknown Problem: ${JSON.stringify(retJson)}`, { classes: ["error"] })
      loading.set(false)
      return
    }

    if (isDeal) await invalidate("deal:detail")
    else await invalidate("investor:detail")

    reply = ""
    loading.set(false)
  }

  async function resolveThread() {
    loading.set(true)

    const ret = await fetch(
      `/api/workflow_info/${isDeal ? "deal" : "investor"}/${info.id}/resolve/`,
      {
        method: "POST",
        credentials: "include",
        headers: {
          "X-CSRFToken": await getCsrfToken(),
          "Content-Type": "application/json",
        },
      },
    )
    const retJson = await ret.json()
    if (!ret.ok || !retJson.ok) {
      toast.push(`Unknown Problem: ${JSON.stringify(retJson)}`, { classes: ["error"] })
      loading.set(false)
      return
    }

    if (isDeal) await invalidate("deal:detail")
    else await invalidate("investor:detail")

    loading.set(false)
  }
</script>

<div
  class="mx-1 mb-2 bg-neutral-200 p-1 text-sm text-gray-800 shadow-md {openThread
    ? 'border-2'
    : ''}  border-yellow-200"
>
  <div class="flex justify-between">
    <span class="font-semibold">
      {dayjs(info.timestamp).format("YYYY-MM-DD HH:mm")}
    </span>
    <span class="inline-flex items-center">
      {$allUsers.find(u => u.id === info.from_user_id)?.username ?? ""}
      {#if info.to_user_id}
        <ArrowLongRightIcon class="mx-0.5 h-4 w-4" />
        {$allUsers.find(u => u.id === info.to_user_id)?.username ?? ""}
      {/if}
    </span>
  </div>

  <div class="flex items-center gap-1" class:my-1={!cleanedComment}>
    {#if info.status_before !== info.status_after}
      {#if info.status_before}
        <div class="inline-block bg-gray-500 px-1.5 text-[13px] text-white">
          {info.status_before}
        </div>
        <ArrowLongRightIcon class="inline-block h-4 w-4" />
      {/if}
      <div class="inline-block bg-pelorous px-1.5 text-[13px] text-white">
        {info.status_after}
      </div>
    {/if}
    {#if confidentialStatusChange}
      <div
        class="inline-block px-1.5 text-[13px] text-white {confidentialStatusChange}"
      >
        {$_("Confidential")}
      </div>
    {/if}
  </div>
  {#if cleanedComment}
    <div class="relative whitespace-pre-line py-1 pr-5">
      {cleanedComment}
    </div>
    <div class="relative ml-3 border">
      <ul class="divide-y-2 bg-neutral-100">
        {#each info.replies as rep}
          <li class="p-1">
            <span class="flex justify-between">
              <span class="font-semibold">
                {dayjs(rep.timestamp).format("YYYY-MM-DD HH:mm")}
              </span>
              <span class="inline-flex items-center">
                {$allUsers.find(u => u.id === rep.user_id)?.username ?? rep.user_id}
              </span>
            </span>
            {rep.comment}
          </li>
        {/each}
      </ul>

      {#if openThread}
        <form
          transition:slide
          class="flex items-center"
          on:submit|preventDefault={sendReply}
        >
          <input
            bind:value={reply}
            type="text"
            class="inpt"
            placeholder={$_("Reply")}
            required
          />
          <button
            class="btn btn-pelorous -ml-0.5 inline-flex h-[34px] items-center gap-2 px-2"
            type="submit"
          >
            <ChatBubbleLeftIcon class="h-5 w-5" />
          </button>
        </form>
      {/if}
      {#if openThread && info.from_user_id === $page.data.user.id}
        <button
          class="btn btn-primary btn-slim ml-auto mr-1 mt-1 flex items-center gap-1"
          type="button"
          on:click={resolveThread}
        >
          {$_("Resolve thread")}
          <CheckCircleIcon class="h-4 w-4" />
        </button>
      {/if}
    </div>
  {/if}
</div>
