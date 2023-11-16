<script lang="ts">
  import dayjs from "dayjs"
  import { _ } from "svelte-i18n"

  import { allUsers } from "$lib/stores"
  import type { DealHull } from "$lib/types/newtypes"

  import CheckCircleIcon from "$components/icons/CheckCircleIcon.svelte"
  import CircleIcon from "$components/icons/CircleIcon.svelte"

  import { stateMap } from "./utils"

  export let deal: DealHull
  export let dealID: number
  export let dealVersion: number | undefined
  let compareFrom: number
  let compareTo: number
</script>

<section>
  <h3>{$_("Version history")}</h3>
  <table class="relative w-full table-auto border-b-2">
    <thead>
      <tr>
        <th>{$_("ID")}</th>
        <th>{$_("Created")}</th>
        <th>{$_("Sent to review")}</th>
        <th>{$_("Reviewed")}</th>
        <th>{$_("Activated")}</th>
        <th>{$_("Fully updated")}</th>
        <th>{$_("Status")}</th>
        <th class="text-right">
          {$_("Show")} /
          <a
            class="text-nowrap"
            href={`/deal/${dealID}/compare/${compareFrom}/${compareTo}/`}
          >
            {$_("Compare")}
          </a>
        </th>
      </tr>
    </thead>
    <tbody>
      {#each deal.versions as version}
        <tr class="odd:bg-gray-100 dark:odd:bg-gray-700">
          <td>{version.id}</td>
          <td>
            {dayjs(version.created_at).format("YYYY-MM-DD HH:mm")}
            <br />
            {#if version.created_by_id}
              {@const user = $allUsers.find(u => u.id === version.created_by_id)}

              {user?.full_name ?? user?.username ?? "-"}
            {/if}
          </td>

          <td>
            {version.sent_to_review_at
              ? dayjs(version.sent_to_review_at).format("YYYY-MM-DD HH:mm")
              : ""}
            <br />
            {#if version.sent_to_review_by_id}
              {$allUsers.find(u => u.id === version.sent_to_review_by_id)?.full_name ??
                "-"}
            {/if}
          </td>
          <td>
            {version.reviewed_at
              ? dayjs(version.reviewed_at).format("YYYY-MM-DD HH:mm")
              : ""}
            <br />
            {#if version.reviewed_by_id}
              {$allUsers.find(u => u.id === version.reviewed_by_id)?.full_name ?? "-"}
            {/if}
          </td>
          <td>
            {version.activated_at
              ? dayjs(version.activated_at).format("YYYY-MM-DD HH:mm")
              : ""}
            <br />
            {#if version.activated_by_id}
              {$allUsers.find(u => u.id === version.activated_by_id)?.full_name ?? "-"}
            {/if}
          </td>
          <td class="px-4">
            {#if version.fully_updated}
              <div title={$_("Fully updated")}>
                <CheckCircleIcon />
              </div>
            {:else}
              <div title={$_("Updated")}>
                <CircleIcon />
              </div>
            {/if}
          </td>

          <td>
            {$stateMap[version.status]}
          </td>
          <td class="whitespace-nowrap text-right">
            {#if dealVersion ? dealVersion === version.id : deal.hull.active_version_id === version.id}
              {$_("Current")}
            {:else}
              <a href="/deal/{dealID}/{version.id}/">{$_("Show")}</a>
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
        <td />
        <td />
        <td />
        <td />
        <td />
        <td />
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
