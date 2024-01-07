<script lang="ts">
  import dayjs from "dayjs"
  import { _ } from "svelte-i18n"

  import { stateMap } from "$lib/newUtils"
  import { allUsers } from "$lib/stores"
  import type { InvestorHull } from "$lib/types/newtypes"

  import CheckCircleIcon from "$components/icons/CheckCircleIcon.svelte"
  import CircleIcon from "$components/icons/CircleIcon.svelte"

  export let investor: InvestorHull
  export let investorID: number
  export let investorVersion: number | undefined
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
        <th>{$_("Modified")}</th>
        <th>{$_("Sent to review")}</th>
        <th>{$_("Reviewed")}</th>
        <th>{$_("Activated")}</th>
        <th>{$_("Fully updated")}</th>
        <th>{$_("Status")}</th>
        <th class="text-right">
          {$_("Show")} /
          <a
            class="text-nowrap"
            href={`/investor/${investorID}/compare/${compareFrom}/${compareTo}/`}
          >
            {$_("Compare")}
          </a>
        </th>
      </tr>
    </thead>
    <tbody>
      {#each investor.versions as version}
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
            {version.modified_at
              ? dayjs(version.modified_at).format("YYYY-MM-DD HH:mm")
              : "-"}
            <br />
            {#if version.modified_by_id}
              {@const user = $allUsers.find(u => u.id === version.modified_by_id)}
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
            {version.sent_to_activation_at
              ? dayjs(version.sent_to_activation_at).format("YYYY-MM-DD HH:mm")
              : ""}
            <br />
            {#if version.sent_to_activation_by_id}
              {$allUsers.find(u => u.id === version.sent_to_activation_by_id)
                ?.full_name ?? "-"}
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
            {#if investorVersion ? investorVersion === version.id : investor.active_version_id === version.id}
              {$_("Current")}
            {:else}
              <a href="/investor/{investorID}/{version.id}/">{$_("Show")}</a>
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
