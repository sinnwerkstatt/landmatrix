<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import { stateMap } from "$lib/newUtils"
  import { type DealHull, type InvestorHull } from "$lib/types/data"
  import { isReporterOrAbove } from "$lib/utils/permissions"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import CheckCircleIcon from "$components/icons/CheckCircleIcon.svelte"
  import CircleIcon from "$components/icons/CircleIcon.svelte"

  interface Props {
    obj: DealHull | InvestorHull
    investorColors?: boolean
  }

  let { obj, investorColors = false }: Props = $props()

  const isDeal = "fully_updated_at" in obj
  const objType = isDeal ? "deal" : "investor"

  let reporterOrHigher = $derived(isReporterOrAbove(page.data.user))

  let compareFrom = $state(obj.versions[1]?.id)
  let compareTo = $state(obj.versions[0]?.id)
</script>

<section>
  <h3 class="heading4">{$_("Version history")}</h3>
  <table class="relative mb-6 w-full table-auto">
    <thead>
      <tr>
        <th>{$_("ID")}</th>
        <th>{$_("Created")}</th>
        <th>{$_("Modified")}</th>
        <th>{$_("Sent to review")}</th>
        <th>{$_("Reviewed")}</th>
        <th>{$_("Activated")}</th>
        {#if isDeal}<th>{$_("Fully updated")}</th>{/if}
        {#if reporterOrHigher}<th>{$_("Status")}</th>{/if}
        <th class="text-right">
          {$_("Show")} /
          {#if compareFrom && compareTo}
            <a
              class:investor={investorColors}
              class="text-nowrap"
              href={`/${objType}/${obj.id}/compare/${compareFrom}/${compareTo}/`}
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
      {#each obj.versions as version}
        <tr class="odd:bg-gray-50 dark:odd:bg-gray-700">
          <td class="p-1">{version.id}</td>
          <td class="p-1">
            <DisplayField
              fieldname="created_at"
              value={version.created_at}
              wrapperClass=""
              valueClass=""
            />
            {#if reporterOrHigher}
              <DisplayField
                fieldname="created_by_id"
                value={version.created_by_id}
                wrapperClass=""
                valueClass=""
              />
            {/if}
          </td>
          <td class="p-1">
            <DisplayField
              fieldname="modified_at"
              value={version.modified_at}
              wrapperClass=""
              valueClass=""
            />
            <!-- TODO: Remove modified_by everywhere (see: #825) -->
            <!--{#if reporterOrHigher}-->
            <!--  <DisplayField-->
            <!--    fieldname="modified_by_id"-->
            <!--    value={version.modified_by_id}-->
            <!--    wrapperClass=""-->
            <!--    valueClass=""-->
            <!--  />-->
            <!--{/if}-->
          </td>
          <td class="p-1">
            <DisplayField
              fieldname="sent_to_review_at"
              value={version.sent_to_review_at}
              wrapperClass=""
              valueClass=""
            />
            {#if reporterOrHigher}
              <DisplayField
                fieldname="sent_to_review_by_id"
                value={version.sent_to_review_by_id}
                wrapperClass=""
                valueClass=""
              />
            {/if}
          </td>
          <td class="p-1">
            <DisplayField
              fieldname="sent_to_activation_at"
              value={version.sent_to_activation_at}
              wrapperClass=""
              valueClass=""
            />
            {#if reporterOrHigher}
              <DisplayField
                fieldname="sent_to_activation_by_id"
                value={version.sent_to_activation_by_id}
                wrapperClass=""
                valueClass=""
              />
            {/if}
          </td>
          <td class="p-1">
            <DisplayField
              fieldname="activated_at"
              value={version.activated_at}
              wrapperClass=""
              valueClass=""
            />
            {#if reporterOrHigher}
              <DisplayField
                fieldname="activated_by_id"
                value={version.activated_by_id}
                wrapperClass=""
                valueClass=""
              />
            {/if}
          </td>
          {#if isDeal}
            <td class="p-1 px-4">
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
          {/if}
          {#if reporterOrHigher}
            <td class="p-1">
              {$stateMap[version.status].title}
            </td>
          {/if}
          <td class="whitespace-nowrap p-1 text-right">
            {#if obj.selected_version.id ? obj.selected_version.id === version.id : obj.active_version_id === version.id}
              {$_("Current")}
            {:else}
              <a
                class:investor={investorColors}
                href="/{objType}/{obj.id}/{version.id}/"
              >
                {$_("Show")}
              </a>
            {/if}
            <span class="ml-4 whitespace-nowrap text-right">
              <input
                bind:group={compareFrom}
                name="versionFrom"
                type="radio"
                class={investorColors ? "rdio investor" : "rdio deal"}
                value={version?.id}
                disabled={version?.id >= compareTo}
              />

              <input
                bind:group={compareTo}
                type="radio"
                name="versionTo"
                class={investorColors ? "rdio investor" : "rdio deal"}
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
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        {#if isDeal}<td></td>{/if}
        {#if reporterOrHigher}<td></td>{/if}
        {#if compareFrom && compareTo}
          <td class="pt-3 text-right">
            <a
              href={`/${objType}/${obj.id}/compare/${compareFrom}/${compareTo}/`}
              class="btn text-nowrap {investorColors ? 'btn-secondary' : 'btn-primary'}"
            >
              {$_("Compare versions")}
            </a>
          </td>
        {/if}
      </tr>
    </tfoot>
  </table>
</section>
