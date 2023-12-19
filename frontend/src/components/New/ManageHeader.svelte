<script lang="ts">
  import dayjs from "dayjs"
  import { _ } from "svelte-i18n"

  import type { DealHull, InvestorHull } from "$lib/types/newtypes.js"
  import { Version2Status } from "$lib/types/newtypes.js"

  import DetailsSummary from "$components/DetailsSummary.svelte"
  import HeaderDates from "$components/HeaderDates.svelte"
  import Cog6ToothIcon from "$components/icons/Cog6ToothIcon.svelte"
  import ManageHeaderLogbook from "$components/New/ManageHeaderLogbook.svelte"
  import ManageHeaderVersionFlow from "$components/New/ManageHeaderVersionFlow.svelte"

  export let object: DealHull | InvestorHull
</script>

<div class="my-4 grid grid-cols-2 lg:grid-cols-3">
  <div class="col-span-2 rounded-tl bg-gray-100">
    <div class="flex items-center justify-between gap-4 p-2">
      <div>
        <h1 class="heading4 my-0 text-[1.875rem]">
          <slot name="heading" />
        </h1>
      </div>

      <DetailsSummary>
        <div class="btn flex items-center gap-1" slot="summary">
          <Cog6ToothIcon />
          actions
        </div>
        <ul
          class="absolute z-50 border border-black bg-white p-2 shadow-2xl"
          slot="details"
        >
          <li>
            <div class="flex items-center gap-2">
              <a class="btn" href="">copy deal</a>
              this will copy the current deal and create blablabla...
            </div>
          </li>
          <li>
            <div class="flex items-center gap-2">
              <a class="btn bg-red-500" href="">delete</a>
              this will mark the deal as deleted. only admins will be able to see it, it
              wont count towards any metrics
            </div>
          </li>
          <li>
            <div class="flex items-center gap-2">
              <a class="btn bg-red-700" href="">set confidential</a>
              this will copy the current deal and create blablabla...
            </div>
          </li>
        </ul>
      </DetailsSummary>
      <DetailsSummary>
        <div class="btn flex items-center gap-1" slot="summary">
          <Cog6ToothIcon />
          versions
        </div>
        <ul
          class="absolute z-50 border border-black bg-white p-2 shadow-2xl"
          slot="details"
        >
          {#if object.active_version}
            <li>
              <div class="flex items-center gap-2">
                <a class="btn" href="/deal/{object.id}/{object.active_version}/">
                  active version
                </a>
                go to current active version
              </div>
            </li>
          {/if}
          {#if object.draft_version}
            <li>
              <div class="flex items-center gap-2">
                <a class="btn" href="/deal/{object.id}/{object.draft_version}/">
                  draft version
                </a>
                go to current draft version
              </div>
            </li>
          {/if}
        </ul>
      </DetailsSummary>
      <HeaderDates obj={object} />
      <!--      <div class="bg-white px-4 py-2">Draft version</div>-->
    </div>
    <hr class="h-0.5 bg-black" />
    <div class="p-2 py-4">
      {#if object.deleted}
        <div
          class="flex flex-col items-center justify-center gap-1 bg-red-500 py-2 text-white"
        >
          <div class="heading4 mb-0">{$_("Deleted")}</div>
          <span>{object.deleted_comment}</span>
        </div>
      {:else if object.confidential}
        <div
          class="flex flex-col items-center justify-center gap-1 bg-red-700 py-2 text-white"
        >
          <div class="heading4 mb-0">{$_("Confidential")}</div>
          <span>{object.confidential_comment}</span>
        </div>
      {:else}
        <div class="mb-4 flex items-center justify-between gap-4">
          <h2 class="heading4 mb-0">Version #{object.selected_version.id}</h2>
          <slot name="visibility" />
        </div>
        {#if object.selected_version.status === Version2Status.ACTIVATED}
          <div
            class="flex flex-col items-center justify-center gap-1 bg-green-700 py-2 text-white"
          >
            <div class="heading4 mb-0">{$_("Activated")}</div>
            <div class="">
              {dayjs(object.selected_version.activated_at).format("YYYY-MM-DD")}
            </div>
          </div>
        {:else}
          <ManageHeaderVersionFlow {object} />
        {/if}
      {/if}
    </div>
  </div>
  <ManageHeaderLogbook {object} extraUserIDs={[]} />
</div>
