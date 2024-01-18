<script lang="ts">
  import dayjs from "dayjs"
  import { _ } from "svelte-i18n"

  import { stateMap } from "$lib/newUtils"
  import type { DealHull } from "$lib/types/newtypes"

  import UserField from "$components/Fields/Display2/UserField.svelte"
  import CheckCircleIcon from "$components/icons/CheckCircleIcon.svelte"
  import CircleIcon from "$components/icons/CircleIcon.svelte"

  export let deal: DealHull
  export let dealID: number
  export let dealVersion: number | undefined
  let compareFrom: number = deal.versions[1]?.id
  let compareTo: number = deal.versions[0]?.id
</script>

<section>
  <h3 class="heading3">{$_("Version history")}</h3>
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
          {#if compareFrom && compareTo}
            <a
              class="text-nowrap"
              href={`/deal/${dealID}/compare/${compareFrom}/${compareTo}/`}
            >
              {$_("Compare")}
            </a>
          {:else}
            {$_("Compare")}
          {/if}
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
            <UserField
              value={version.created_by_id}
              fieldname="created_by_id"
              wrapperClass=""
              valueClass=""
            />
          </td>
          <td>
            {version.modified_at
              ? dayjs(version.modified_at).format("YYYY-MM-DD HH:mm")
              : ""}
            <br />
            <UserField
              value={version.modified_by_id}
              fieldname="modified_by_id"
              wrapperClass=""
              valueClass=""
            />
          </td>
          <td>
            {version.sent_to_review_at
              ? dayjs(version.sent_to_review_at).format("YYYY-MM-DD HH:mm")
              : ""}
            <br />
            <UserField
              value={version.sent_to_review_by_id}
              fieldname="sent_to_review_by_id"
              wrapperClass=""
              valueClass=""
            />
          </td>
          <td>
            {version.sent_to_activation_at
              ? dayjs(version.sent_to_activation_at).format("YYYY-MM-DD HH:mm")
              : ""}
            <UserField
              value={version.sent_to_activation_by_id}
              fieldname="sent_to_activation_by_id"
              wrapperClass=""
              valueClass=""
            />
          </td>
          <td>
            {version.activated_at
              ? dayjs(version.activated_at).format("YYYY-MM-DD HH:mm")
              : ""}
            <UserField
              value={version.activated_by_id}
              fieldname="activated_by_id"
              wrapperClass=""
              valueClass=""
            />
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
            {#if dealVersion ? dealVersion === version.id : deal.active_version_id === version.id}
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
        <td />
        {#if compareFrom && compareTo}
          <td class="text-right">
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
