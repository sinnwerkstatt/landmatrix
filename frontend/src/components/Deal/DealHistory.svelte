<script lang="ts">
  import dayjs from "dayjs"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { draftStatusMap, statusMap } from "$lib/stores"
  import type { Deal, DealVersion } from "$lib/types/deal"
  import { DraftStatus, Status } from "$lib/types/generics"

  import CheckCircleIcon from "$components/icons/CheckCircleIcon.svelte"
  import CircleIcon from "$components/icons/CircleIcon.svelte"

  export let deal: Deal
  export let dealID: number
  export let dealVersion: number

  let compareFrom
  let compareTo

  onMount(() => {
    if (deal.versions?.length >= 2) {
      compareTo = deal.versions[0].id
      compareFrom = deal.versions[1].id
    }
  })

  function calcVersionList(versions: DealVersion[]) {
    versions = JSON.parse(JSON.stringify(versions))
    if (!$page.data.user?.is_authenticated) {
      versions = versions.filter(v => !(v.deal.confidential || v.deal.draft_status))
    }
    let currentActive = false
    return versions.map(v => {
      if (!v.deal.draft_status && !currentActive) {
        v.link = `/deal/${dealID}`
        currentActive = true
      } else v.link = `/deal/${dealID}/${v.id}`
      return v
    })
  }

  let enrichedVersions
  $: enrichedVersions = calcVersionList(deal.versions ?? [])

  function calcDeducedPosition(versions) {
    if (versions.length === 0) return 0
    if (dealVersion) {
      return versions.findIndex(v => +v.id === +dealVersion)
    }
    for (const [i, v] of versions.entries()) {
      if (v.deal.draft_status === null) return i
    }
    return versions.length - 1
  }

  let deducedPosition: number
  $: deducedPosition = calcDeducedPosition(deal?.versions)

  function deriveStatus(status: Status, draft_status: DraftStatus) {
    return draft_status ? $draftStatusMap[draft_status] : $statusMap[status]
  }
</script>

<section>
  <h3>{$_("Version history")}</h3>
  <table class="relative w-full table-auto border-b-2">
    <thead>
      <tr>
        <th>{$_("Created")}</th>
        {#if $page.data.user?.is_authenticated}
          <th>{$_("User")}</th>
        {/if}
        <th>{$_("Fully updated")}</th>
        {#if $page.data.user?.is_authenticated}
          <th>{$_("Status")}</th>
        {/if}
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
      {#each enrichedVersions as version, i}
        <tr class="odd:bg-gray-100 dark:odd:bg-gray-700">
          <td>{dayjs(version.created_at).format("YYYY-MM-DD HH:mm")}</td>
          {#if $page.data.user?.is_authenticated}
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
          {#if $page.data.user?.is_authenticated}
            <td>
              {deriveStatus(version?.deal?.status, version?.deal?.draft_status)}
            </td>
          {/if}
          <td class="whitespace-nowrap text-right">
            {#if i === deducedPosition}
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
        {#if $page.data.user?.is_authenticated}
          <td />
        {/if}
        <td />
        {#if $page.data.user?.is_authenticated}
          <td />
        {/if}
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
