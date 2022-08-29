<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { formfields } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import type { WorkflowInfo } from "$lib/types/generics"
  import type { Investor } from "$lib/types/investor"

  import DateTimeField from "$components/Fields/Display/DateTimeField.svelte"
  import ForeignKeyField from "$components/Fields/Display/ForeignKeyField.svelte"
  import StatusField from "$components/Fields/Display/StatusField.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import StarIcon from "$components/icons/StarIcon.svelte"

  export let objects: Array<Deal | Investor>
  export let model: "deal" | "investor" = "deal"

  $: objectsWInfo = objects.map(obj => {
    const wfis = obj.workflowinfos as WorkflowInfo[]
    let relevantWFI = wfis.find(
      wfi =>
        wfi.draft_status_before === wfi.draft_status_after &&
        wfi.to_user?.id === $page.data.user.id,
    )

    // const openReq =
    //   d.current_draft_id === relevantWFI?.deal_version_id && d.draft_status === 1;

    return { ...obj, relevantWFI }
  })
  // .sort((a, b) => {
  //   if (a.openReq && !b.openReq) return -1;
  //   else if (b.openReq && !a.openReq) return 1;
  //   if (!b.relevantWFI?.timestamp || !a.relevantWFI?.timestamp) return 0;
  //   return new Date(b.relevantWFI.timestamp) - new Date(a.relevantWFI.timestamp);
  // });
</script>

<table>
  <thead>
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
      <th class="px-3 py-1">Comment</th>
      <!--      <th>{$formfields.deal["created_at"].label}</th>-->
      <!--      <th>{$formfields.deal["created_by"].label}</th>-->
      <!--      <th>{$formfields.deal["modified_at"].label}</th>-->
      <!--      <th>{$formfields.deal["modified_by"].label}</th>-->
    </tr>
  </thead>
  <tbody>
    {#each objectsWInfo as obj}
      <tr class:font-bold={obj.openReq}>
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
        <td class="px-3 py-1">
          {obj.relevantWFI?.comment}
        </td>
      </tr>
    {/each}
  </tbody>
</table>
