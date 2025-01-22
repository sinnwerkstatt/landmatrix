<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import dayjs from "dayjs"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { invalidate } from "$app/navigation"
  import { page } from "$app/state"

  import { stateMap } from "$lib/newUtils"
  import { loading } from "$lib/stores/basics"
  import type { WorkflowInfo } from "$lib/types/data"
  import { getCsrfToken } from "$lib/utils"

  import UserField from "$components/Fields/Display2/UserField.svelte"
  import ArrowLongRightIcon from "$components/icons/ArrowLongRightIcon.svelte"
  import ChatBubbleLeftIcon from "$components/icons/ChatBubbleLeftIcon.svelte"
  import CheckCircleIcon from "$components/icons/CheckCircleIcon.svelte"

  interface Props {
    info: WorkflowInfo
    isDeal?: boolean
  }

  let { info, isDeal = true }: Props = $props()

  let confidentialStatusChange = $derived(
    info.comment?.startsWith("[SET_CONFIDENTIAL]")
      ? "bg-red-400"
      : info.comment?.startsWith("[UNSET_CONFIDENTIAL]")
        ? "bg-green-600 line-through"
        : false,
  )

  let cleanedComment = $derived(
    info.comment
      ?.replace("[SET_CONFIDENTIAL]", "")
      .replace("[UNSET_CONFIDENTIAL] ", ""),
  )

  let openThread = $derived(
    info.status_after === info.status_before &&
      info.to_user_id &&
      [info.to_user_id, info.from_user_id].includes(page.data.user?.id as number) &&
      !info.resolved,
  )

  let reply = $state("")

  async function onsubmit(e: SubmitEvent) {
    e.preventDefault()

    loading.set(true)

    if ((e.submitter as HTMLButtonElement).name === "submitandresolve") {
      if (reply) await sendReply()
      await resolveThread()
    } else {
      await sendReply()
    }

    loading.set(false)
  }

  async function sendReply() {
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
      return
    }

    if (isDeal) await invalidate("deal:detail")
    else await invalidate("investor:detail")

    reply = ""
  }

  async function resolveThread() {
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
      return
    }

    if (isDeal) await invalidate("deal:detail")
    else await invalidate("investor:detail")
  }
</script>

<div
  class="mx-1 mb-2 border-yellow-200 bg-neutral-200 p-1 text-sm text-gray-800 shadow-md"
  class:border-2={openThread}
>
  <div class="flex justify-between">
    <span class="font-semibold">
      {dayjs(info.timestamp).format("YYYY-MM-DD HH:mm")}
    </span>
    <span class="inline-flex items-center">
      <UserField value={info.from_user_id} />
      {#if info.to_user_id}
        <ArrowLongRightIcon class="mx-0.5 h-4 w-4" />
        <UserField value={info.to_user_id} />
      {/if}
    </span>
  </div>

  <div class="flex items-center gap-1" class:my-1={!cleanedComment}>
    {#if info.status_before !== info.status_after}
      {#if info.status_before}
        {@const before = $stateMap[info.status_before]}
        <div class="inline-block px-1.5 text-[13px] {before.classes}">
          {before.title}
        </div>
        {#if info.status_after}
          <ArrowLongRightIcon class="inline-block h-4 w-4" />
        {/if}
      {/if}
      {#if info.status_after}
        {@const after = $stateMap[info.status_after]}
        <div class="inline-block px-1.5 text-[13px] {after.classes}">
          {after.title}
        </div>
      {/if}
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
                <UserField value={rep.user_id} />
              </span>
            </span>
            {rep.comment}
          </li>
        {/each}
      </ul>

      {#if openThread}
        <form transition:slide {onsubmit}>
          <div class="flex items-center">
            <input
              bind:value={reply}
              type="text"
              class="inpt"
              placeholder={$_("Reply")}
            />
            <button
              class="btn btn-pelorous -ml-0.5 inline-flex h-[34px] items-center gap-2 px-2 text-sm"
              type="submit"
              disabled={!reply}
            >
              {$_("Send")}
              <ChatBubbleLeftIcon class="h-4 w-4" />
            </button>
          </div>
          {#if info.from_user_id === page.data.user?.id}
            <button
              class="btn btn-primary btn-flat ml-auto mr-1 mt-1 flex items-center gap-1"
              type="submit"
              name="submitandresolve"
            >
              {#if reply}
                {$_("Send")} &amp;
              {/if}
              {$_("Resolve thread")}
              <CheckCircleIcon class="h-4 w-4" />
            </button>
          {/if}
        </form>
      {/if}
    </div>
  {/if}
</div>
