<script lang="ts">
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import { formfields } from "$lib/stores.js";
  import type { Deal, DealWorkflowInfo } from "$lib/types/deal";
  import DateTimeField from "$components/Fields/Display/DateTimeField.svelte";
  import ForeignKeyField from "$components/Fields/Display/ForeignKeyField.svelte";
  import StatusField from "$components/Fields/Display/StatusField.svelte";
  import DisplayField from "$components/Fields/DisplayField.svelte";
  import StarIcon from "$components/icons/StarIcon.svelte";

  export let deals: Deal[];

  $: dealsWInfo = deals
    .map((d) => {
      const wfis = d.workflowinfos as DealWorkflowInfo[];
      let improveWFI = wfis.find(
        (wfi) =>
          [2, 3].includes(wfi.draft_status_before) &&
          wfi.draft_status_after === 1 &&
          wfi.from_user?.id === $page.data.user.id
      );

      const openReq =
        d.draft_id === improveWFI?.deal_version_id && d.draft_status === 1;

      return { ...d, improveWFI, openReq };
    })
    .sort((a, b) => {
      if (a.openReq && !b.openReq) return -1;
      else if (b.openReq && !a.openReq) return 1;
      if (!b.improveWFI?.timestamp || !a.improveWFI?.timestamp) return 0;
      return new Date(b.improveWFI.timestamp) - new Date(a.improveWFI.timestamp);
    });
</script>

<table>
  <thead>
    <tr>
      <th class="px-3 py-1" />
      <th class="px-3 py-1">Date of request</th>
      <th class="px-3 py-1">{$formfields.deal["id"].label}</th>
      <th class="px-3 py-1">{$formfields.deal["country"].label}</th>
      <th class="px-3 py-1">{$formfields.deal["deal_size"].label}</th>
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
    {#each dealsWInfo as deal}
      <tr class:font-bold={deal.openReq}>
        <td>
          {#if deal.openReq}
            <div title={$_("Open request")}>
              <StarIcon />
            </div>
          {/if}
        </td>
        <td class="px-3 py-1">
          <DateTimeField value={deal.improveWFI?.timestamp} format="YYYY-MM-DD HH:mm" />
        </td>
        <td class="px-3 py-1">
          <DisplayField
            wrapperClasses="p-1"
            valueClasses=""
            fieldname="id"
            value={deal.id}
            objectVersion={deal.draft_id}
          />
        </td>
        <td class="px-3 py-1">
          <DisplayField
            wrapperClasses="p-1"
            valueClasses=""
            fieldname="country"
            value={deal.country}
          />
        </td>
        <td class="px-3 py-1">
          <DisplayField
            wrapperClasses="p-1"
            valueClasses=""
            fieldname="deal_size"
            value={deal.deal_size}
          />
        </td>
        <td class="px-3 py-1">
          <StatusField status={deal.status} draft_status={deal.draft_status} />
        </td>
        <td class="px-3 py-1">
          <ForeignKeyField value={deal.improveWFI?.from_user} formfield={{}} />
        </td>
        <td class="px-3 py-1">
          <ForeignKeyField value={deal.improveWFI?.to_user} formfield={{}} />
        </td>
        <td class="px-3 py-1">
          {deal.improveWFI?.comment}
        </td>
      </tr>
    {/each}
  </tbody>
</table>
