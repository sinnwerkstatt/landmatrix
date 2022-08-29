<script lang="ts">
  import dayjs from "dayjs";
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import type { Investor, InvestorVersion } from "$lib/types/investor";

  export let investor: Investor;
  export let investorID: number;
  export let investorVersion: number;

  let compareFrom;
  let compareTo;

  onMount(() => {
    if (investor.versions?.length >= 2) {
      compareTo = investor.versions[0].id;
      compareFrom = investor.versions[1].id;
    }
  });

  function calcVersionList(versions: InvestorVersion[]) {
    versions = JSON.parse(JSON.stringify(versions));
    if (!$page.data.user.is_authenticated) {
      versions = versions.filter(
        (v) => !(v.investor.confidential || v.investor.draft_status)
      );
    }
    let currentActive = false;
    return versions.map((v) => {
      if (!v.investor.draft_status && !currentActive) {
        v.link = `/investor/${investorID}`;
        currentActive = true;
      } else v.link = `/investor/${investorID}/${v.id}`;
      return v;
    });
  }
  $: enriched_versions = calcVersionList(investor.versions ?? []);

  function calcDeducedPosition(versions) {
    if (versions.length === 0) return 0;
    if (investorVersion) {
      return versions.findIndex((v) => +v.id === +investorVersion);
    }
    for (const [i, v] of versions.entries()) {
      if (v.investor.draft_status === null) return i;
    }
    return versions.length - 1;
  }

  $: deduced_position = calcDeducedPosition(investor?.versions);

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
  <table class="relative w-full table-auto border-b-2">
    <thead>
      <tr>
        <th>{$_("Created")}</th>
        {#if $page.data.user.is_authenticated} <th>{$_("User")}</th> {/if}
        {#if $page.data.user.is_authenticated} <th>{$_("Status")}</th> {/if}
        <th class="text-right">
          {$_("Show")} /
          <a
            href={`/investor/${investorID}/compare/${compareFrom}/${compareTo}/`}
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

          {#if $page.data.user.is_authenticated}
            <td>
              {$_(
                derive_status(
                  version?.investor?.status,
                  version?.investor?.draft_status
                )
              )}
            </td>
          {/if}
          <td class="whitespace-nowrap text-right">
            {#if i === deduced_position}
              {$_("Current")}
            {:else}
              <a href={version?.link}>{$_("Show")}</a>
            {/if}
            <span class="ml-4 whitespace-nowrap text-right">
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
              href={`/investor/${investorID}/compare/${compareFrom}/${compareTo}/`}
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
