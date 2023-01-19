<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { formfields } from "$lib/stores"
  import type { Deal, DealWorkflowInfo } from "$lib/types/deal"
  import { DraftStatus } from "$lib/types/generics"
  import type { Investor } from "$lib/types/investor"

  import DateTimeField from "$components/Fields/Display/DateTimeField.svelte"
  import ForeignKeyField from "$components/Fields/Display/ForeignKeyField.svelte"
  import StatusField from "$components/Fields/Display/StatusField.svelte"
  import WorkflowInfosField from "$components/Fields/Display/WorkflowInfosField.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import StarIcon from "$components/icons/StarIcon.svelte"

  export let objects: Array<Deal | Investor>
  export let model: "deal" | "investor" = "deal"

  $: objectsWInfo = objects
    .map(obj => {
      const wfis = obj.workflowinfos as DealWorkflowInfo[]
      let relevantWFI = wfis.find(
        wfi =>
          (wfi.draft_status_before === DraftStatus.REVIEW ||
            wfi.draft_status_before === DraftStatus.ACTIVATION) &&
          wfi.draft_status_after === DraftStatus.DRAFT &&
          wfi.from_user?.id === $page.data.user.id,
      )

      return { ...obj, relevantWFI }
    })
    .sort((a, b) => {
      if (!b.relevantWFI?.timestamp || !a.relevantWFI?.timestamp) return 0
      return new Date(b.relevantWFI.timestamp) - new Date(a.relevantWFI.timestamp)
    })
</script>

<table class="w-full overflow-x-auto border border-gray-700">
  <thead
    class="cursor-pointer items-center whitespace-nowrap bg-gray-700 p-1 pr-4 font-medium text-white"
  >
    <tr>
      <th class="px-3 py-1" />
      <th class="px-3 py-1">Date of request</th>
      <th class="px-3 py-1">{$formfields[model]["id"].label}</th>
      <th class="px-3 py-1">{$formfields[model]["country"].label}</th>
      {#if model === "deal"}
        <th class="px-3 py-1">{$formfields[model]["deal_size"].label}</th>
      {/if}
      <th class="px-3 py-1">Status</th>

      <th class="px-3 py-1">From user</th>
      <th class="px-3 py-1">To user</th>
      <th class="px-3 py-1">Feedback</th>
    </tr>
  </thead>
  <tbody>
    {#each objectsWInfo as obj}
      <tr
        class:font-bold={obj.openReq}
        class="odd:bg-white even:bg-gray-100 hover:bg-gray-200"
      >
        <td>
          {#if obj.openReq}
            <div title={$_("Open request")}>
              <StarIcon />
            </div>
          {/if}
        </td>
        <td class="px-3 py-1">
          <DateTimeField value={obj.relevantWFI?.timestamp} format="YYYY-MM-DD HH:mm" />
        </td>
        <td class="px-3 py-1">
          <DisplayField
            wrapperClasses="p-1"
            valueClasses=""
            fieldname="id"
            value={obj.id}
            objectVersion={obj.current_draft_id}
            {model}
          />
        </td>
        <td class="px-3 py-1">
          <DisplayField
            wrapperClasses="p-1"
            valueClasses=""
            fieldname="country"
            value={obj.country}
            {model}
          />
        </td>
        {#if model === "deal"}
          <td class="px-3 py-1">
            <DisplayField
              wrapperClasses="p-1"
              valueClasses=""
              fieldname="deal_size"
              value={obj.deal_size}
              {model}
            />
          </td>
        {/if}
        <td class="px-3 py-1">
          <StatusField status={obj.status} draft_status={obj.draft_status} />
        </td>
        <td class="px-3 py-1">
          <ForeignKeyField value={obj.relevantWFI?.from_user} formfield={{}} />
        </td>
        <td class="px-3 py-1">
          <ForeignKeyField value={obj.relevantWFI?.to_user} formfield={{}} />
        </td>
        <td class="relative w-[368px] px-3 py-1">
          <WorkflowInfosField value={obj.workflowinfos}>
            {obj.relevantWFI?.comment}
          </WorkflowInfosField>
        </td>
      </tr>
    {/each}
  </tbody>
</table>
