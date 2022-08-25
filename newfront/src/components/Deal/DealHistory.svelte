<script lang="ts">
  import dayjs from "dayjs";
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import type { Deal, DealVersion } from "$lib/types/deal";
  import CheckCircleIcon from "$components/icons/CheckCircleIcon.svelte";
  import CircleIcon from "$components/icons/CircleIcon.svelte";

  export let deal: Deal;
  export let dealID: number;
  export let dealVersion: number;

  let compareFrom;
  let compareTo;

  onMount(() => {
    if (deal.versions?.length >= 2) {
      compareTo = deal.versions[0].id;
      compareFrom = deal.versions[1].id;
    }
  });

  function calcVersionList(versions: DealVersion[]) {
    versions = JSON.parse(JSON.stringify(versions));
    if (!$page.data.user.is_authenticated) {
      versions = versions.filter((v) => !(v.deal.confidential || v.deal.draft_status));
    }
    let currentActive = false;
    return versions.map((v) => {
      if (!v.deal.draft_status && !currentActive) {
        v.link = `/deal/${dealID}`;
        currentActive = true;
      } else v.link = `/deal/${dealID}/${v.id}`;
      return v;
    });
  }
  $: enriched_versions = calcVersionList(deal.versions ?? []);

  function calcDeducedPosition(versions) {
    if (versions.length === 0) return 0;
    if (dealVersion) {
      return versions.findIndex((v) => +v.id === +dealVersion);
    }
    for (const [i, v] of versions.entries()) {
      if (v.deal.draft_status === null) return i;
    }
    return versions.length - 1;
  }

  $: deduced_position = calcDeducedPosition(deal?.versions);

  const status_map = {
    1: "Draft",
    2: "Active", //"Live",
    3: "Active", // "Updated",
    4: "Deleted",
    5: "Rejected", // legacy
    6: "To Delete", // legacy
  };
  const draft_status_map = {
    1: "Draft",
    2: "Review",
    3: "Activation",
    4: "Rejected", // legacy
    5: "Deleted",
  };
  function derive_status(status, draft_status) {
    return draft_status ? draft_status_map[draft_status] : status_map[status];
  }
</script>

<section>
  <h3>{$_("Version history")}</h3>
  <table class="table-auto w-full border-b-2 relative">
    <thead>
      <tr>
        <th>{$_("Created")}</th>
        {#if $page.data.user.is_authenticated} <th>{$_("User")}</th> {/if}
        <th>{$_("Fully updated")}</th>
        {#if $page.data.user.is_authenticated} <th>{$_("Status")}</th> {/if}
        <th class="text-right">
          {$_("Show")} /
          <a
            href={`/deal/${dealID}/compare/${compareFrom}/${compareTo}/`}
            class="text-nowrap"
          >
            {$_("Compare")}
          </a>
        </th>
      </tr>
    </thead>
    <tbody>
      {#each enriched_versions as version, i}
        <tr class="odd:bg-gray-100">
          <td>{dayjs(version.created_at).format("YYYY-MM-DD HH:mm")}</td>
          {#if $page.data.user.is_authenticated}
            <td>
              {version.created_by && version.created_by.full_name}
            </td>
          {/if}
          <td class="px-4">
            {#if version.deal.fully_updated}
              <div title={$_("Fully updated")}><CheckCircleIcon /></div>
            {:else}
              <div title={$_("Updated")}><CircleIcon /></div>
            {/if}
          </td>
          {#if $page.data.user.is_authenticated}
            <td>
              {$_(derive_status(version?.deal?.status, version?.deal?.draft_status))}
            </td>
          {/if}
          <td class="text-right whitespace-nowrap">
            {#if i === deduced_position}
              {$_("Current")}
            {:else}
              <a href={version?.link}>{$_("Show")}</a>
            {/if}
            <span class="ml-4 text-right whitespace-nowrap">
              <input
                bind:group={compareFrom}
                type="radio"
                value={version?.id}
                disabled={version?.id >= compareTo}
              />

              <input
                bind:group={compareTo}
                type="radio"
                value={version?.id}
                disabled={version?.id <= compareFrom}
              />
            </span>
          </td>
        </tr>
      {/each}
    </tbody>
    <tfoot>
      <tr>
        <td />
        {#if $page.data.user.is_authenticated} <td /> {/if}
        <td />
        {#if $page.data.user.is_authenticated} <td /> {/if}
        {#if compareFrom && compareTo}
          <td>
            <a
              href={`/deal/${dealID}/compare/${compareFrom}/${compareTo}/`}
              class="btn btn-primary text-nowrap"
            >
              {$_("Compare versions")}
            </a>
          </td>
        {/if}
      </tr>
    </tfoot>
  </table>
</section>
