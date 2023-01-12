<script lang="ts">
  import { Client, gql } from "@urql/svelte"
  import { toast } from "@zerodevx/svelte-toast"
  import dayjs from "dayjs"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { invalidateAll } from "$app/navigation"
  import { page } from "$app/stores"

  import { allUsers } from "$lib/stores"
  import type { WorkflowInfo as WFInfo } from "$lib/types/generics"
  import { Status } from "$lib/types/generics"

  import ArrowLongRightIcon from "$components/icons/ArrowLongRightIcon.svelte"
  import ChatBubbleLeftIcon from "$components/icons/ChatBubbleLeftIcon.svelte"
  import CheckCircleIcon from "$components/icons/CheckCircleIcon.svelte"

  export let info: WFInfo
  $: status_map = {
    1: $_("Draft"),
    2: $_("Active"), //"Live",
    3: $_("Active"), // "Updated",
    4: $_("Deleted"),
    5: $_("Rejected"), // legacy
    6: $_("To Delete"), // legacy
  }
  $: draft_status_map = {
    1: $_("Draft"),
    2: $_("Review"),
    3: $_("Activation"),
    4: $_("Rejected"), // legacy
    5: $_("Deleted"),
  }
  $: confidentialStatusChange = info.comment?.startsWith("[SET_CONFIDENTIAL]")
    ? "bg-red-400"
    : info.comment?.startsWith("[UNSET_CONFIDENTIAL]")
    ? "bg-green-600 line-through"
    : false

  $: cleanedComment = info.comment
    ?.replace("[SET_CONFIDENTIAL]", "")
    .replace("[UNSET_CONFIDENTIAL] ", "")

  $: openThread =
    info.draft_status_after === info.draft_status_before &&
    info.to_user &&
    [info.to_user.id, info.from_user.id].includes($page.data.user.id) &&
    !info.resolved

  let reply = ""

  async function sendReply() {
    const { data, error } = await ($page.data.urqlClient as Client)
      .mutation<{ add_workflow_info_reply: boolean }>(
        gql`
          mutation ($id: Int!, $type: String!, $from_user_id: Int!, $comment: String!) {
            add_workflow_info_reply(
              id: $id
              type: $type
              from_user_id: $from_user_id
              comment: $comment
            )
          }
        `,
        {
          id: info.id,
          type: info.__typename,
          from_user_id: $page.data.user.id,
          comment: reply,
        },
      )
      .toPromise()
    if (error) {
      toast.push(`Unknown Problem: ${error}`, { classes: ["error"] })
      return
    }
    if (!data) {
      toast.push(`Unknown Problem: ${error}`, { classes: ["error"] })
      return
    }
    if (data.add_workflow_info_reply) {
      info.replies = [
        ...info.replies,
        {
          timestamp: new Date().toISOString(),
          user_id: $page.data.user.id,
          comment: reply,
        },
      ]
      reply = ""
    }
    await invalidateAll()
  }

  async function resolveThread() {
    const { data, error } = await ($page.data.urqlClient as Client)
      .mutation<{ resolve_workflow_info: boolean }>(
        gql`
          mutation ($id: Int!, $type: String!) {
            resolve_workflow_info(id: $id, type: $type)
          }
        `,
        { id: info.id, type: info.__typename },
      )
      .toPromise()
    if (error) {
      toast.push(`Unknown Problem: ${error}`, { classes: ["error"] })
      return
    }
    if (!data) {
      toast.push(`Unknown Problem: ${error}`, { classes: ["error"] })
      return
    }
    if (data.resolve_workflow_info) {
      info = { ...info, resolved: true }
    }
    await invalidateAll()
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
      {info.from_user.username}
      {#if info.to_user}
        <ArrowLongRightIcon class="mx-0.5 h-4 w-4" />
        {info.to_user.username}
      {/if}
    </span>
  </div>

  <div class="flex items-center gap-1" class:my-1={!cleanedComment}>
    {#if info.draft_status_before !== info.draft_status_after}
      {#if info.draft_status_before}
        <div class="inline-block bg-gray-500 px-1.5 text-[13px] text-white">
          {draft_status_map[info.draft_status_before]}
        </div>
        <ArrowLongRightIcon class="inline-block h-4 w-4" />
      {/if}
      <div class="inline-block bg-pelorous px-1.5 text-[13px] text-white">
        {draft_status_map[info.draft_status_after] || status_map[Status.LIVE]}
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
      {#if openThread && info.from_user.id === $page.data.user.id}
        <button
          class="btn btn-primary btn-slim ml-auto mt-1 mr-1 flex items-center gap-1"
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
