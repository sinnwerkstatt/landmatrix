<script lang="ts">
  import { _ } from "svelte-i18n"

  import { stateMap } from "$lib/newUtils"
  import type { InvestorHull } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  export let investor: InvestorHull
  export let investorID: number
  export let investorVersion: number | undefined
  let compareFrom: number = investor.versions[1]?.id
  let compareTo: number = investor.versions[0]?.id
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
        <th>{$_("Status")}</th>
        <th class="text-right">
          {$_("Show")} /
          {#if compareFrom && compareTo}
            <a
              class="text-nowrap"
              href={`/investor/${investorID}/compare/${compareFrom}/${compareTo}/`}
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
      {#each investor.versions as version}
        <tr class="odd:bg-gray-100 dark:odd:bg-gray-700">
          <td>{version.id}</td>
          <td>
            <DisplayField
              fieldname="created_at"
              value={version.created_at}
              wrapperClass=""
              valueClass=""
            />
            <DisplayField
              fieldname="created_by_id"
              value={version.created_by_id}
              wrapperClass=""
              valueClass=""
            />
          </td>
          <td>
            <DisplayField
              fieldname="modified_at"
              value={version.modified_at}
              wrapperClass=""
              valueClass=""
            />
            <DisplayField
              fieldname="modified_by_id"
              value={version.modified_by_id}
              wrapperClass=""
              valueClass=""
            />
          </td>
          <td>
            <DisplayField
              fieldname="sent_to_review_at"
              value={version.sent_to_review_at}
              wrapperClass=""
              valueClass=""
            />
            <DisplayField
              fieldname="sent_to_review_by_id"
              value={version.sent_to_review_by_id}
              wrapperClass=""
              valueClass=""
            />
          </td>
          <td>
            <DisplayField
              fieldname="sent_to_activation_at"
              value={version.sent_to_activation_at}
              wrapperClass=""
              valueClass=""
            />
            <DisplayField
              fieldname="sent_to_activation_by_id"
              value={version.sent_to_activation_by_id}
              wrapperClass=""
              valueClass=""
            />
          </td>
          <td>
            <DisplayField
              fieldname="activated_at"
              value={version.activated_at}
              wrapperClass=""
              valueClass=""
            />
            <DisplayField
              fieldname="activated_by_id"
              value={version.activated_by_id}
              wrapperClass=""
              valueClass=""
            />
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
