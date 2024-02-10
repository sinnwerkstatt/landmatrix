<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { Counts } from "./caseStatistics"

  export let counts: Counts = {}

  function getRatio(n: number | null | undefined, model = "deal") {
    if (n === null || n === undefined) return ""
    if (model !== "deal") {
      if (!counts.investors_public_count) return " "
      return ((n / counts.investors_public_count ?? 1) * 100).toFixed(1) + " %"
    }
    if (!counts.deals_public_count) return " "
    return ((n / counts.deals_public_count ?? 1) * 100).toFixed(1) + " %"
  }
</script>

<h2 class="heading5 mb-2 pt-3">{$_("Quality goals")}</h2>

<div class="grid grid-cols-2">
  <div>
    <table class="mb-4">
      <thead>
        <tr>
          <th />
          <th class="px-3 py-1">{$_("Count")}</th>
          <th class="px-3 py-1">{$_("Ratio")}</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="py-1 pr-3 font-bold">
            {$_("Publicly visible deals")}
            <sup>1</sup>
          </td>
          <td class="px-3 py-1">{counts.deals_public_count}</td>
          <td />
        </tr>

        <tr>
          <td class="py-1 pr-3 font-bold">
            {$_("Deals with with multiple data sources")}
          </td>
          <td class="px-3 py-1">{counts.deals_public_multi_ds_count}</td>
          <td class="px-3 py-1">{getRatio(counts.deals_public_multi_ds_count)}</td>
        </tr>

        <tr>
          <td class="py-1 pr-3 font-bold">
            {$_("Deals georeferenced with high accuracy")}
            <sup>2</sup>
          </td>
          <td class="px-3 py-1">{counts.deals_public_high_geo_accuracy}</td>
          <td class="px-3 py-1">{getRatio(counts.deals_public_high_geo_accuracy)}</td>
        </tr>

        <tr>
          <td class="py-1 pr-3 text-center font-bold">
            {$_("Deals with polygon data")}
          </td>
          <td class="px-3 py-1">{counts.deals_public_polygons}</td>
          <td class="px-3 py-1">{getRatio(counts.deals_public_polygons)}</td>
        </tr>
      </tbody>
    </table>

    <div>
      <div>
        <sup>1</sup>
        {$_("Active deals with public filter ok, not confidential.")}
      </div>
      <div>
        <sup>2</sup>
        {$_(
          "Deals with at least one location with either accuracy level 'Coordinates' or 'Exact location' or at least one polygon.",
        )}
      </div>
    </div>
  </div>
  <div>
    <table class="mb-4">
      <thead>
        <tr>
          <th />
          <th class="px-3 py-1">{$_("Count")}</th>
          <th class="px-3 py-1">{$_("Ratio")}</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td class="py-1 pr-3 font-bold">
            {$_("Publicly visible investors")}
          </td>
          <td class="px-3 py-1">{counts.investors_public_count}</td>
          <td />
        </tr>

        <tr>
          <td class="py-1 pr-3 font-bold">
            {$_("Investors with name")}
          </td>
          <td class="px-3 py-1">{counts.investors_public_known}</td>
          <td class="px-3 py-1">{getRatio(counts.investors_public_known, "i")}</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
<!--<div class="my-8 flex items-center justify-evenly gap-4 bg-neutral-300 p-2 text-center">-->
<!--  <div class="flex flex-col items-center gap-2">-->
<!--    <div class="bg-neutral-200 p-3 font-bold drop-shadow-lg">-->
<!--      <div class="text-2xl">{counts.deals_public_count}</div>-->
<!--      <div>&nbsp;</div>-->
<!--    </div>-->
<!--    <div>{$_("Publicly visible deals")}</div>-->
<!--    <div class="text-[10px]">-->
<!--      {$_("Active deals with public filter ok, not confidential.")}-->
<!--    </div>-->
<!--  </div>-->
<!--  <div class="flex flex-col items-center gap-2">-->
<!--    <div class="bg-neutral-200 p-3  font-bold drop-shadow-lg">-->
<!--      <div class="text-2xl">{counts.deals_public_multi_ds_count}</div>-->
<!--      <div>{getRatio(counts.deals_public_multi_ds_count)}</div>-->
<!--    </div>-->
<!--    {$_("Deals with with multiple data sources")}-->
<!--    <div class="text-[10px]">&nbsp;</div>-->
<!--  </div>-->
<!--  <div class="flex flex-col items-center gap-2">-->
<!--    <div class="bg-neutral-200 p-3 font-bold drop-shadow-lg">-->
<!--      <div class="text-2xl">{counts.deals_public_high_geo_accuracy}</div>-->
<!--      <div>{getRatio(counts.deals_public_high_geo_accuracy)}</div>-->
<!--    </div>-->
<!--    {$_("Deals georeferenced with high accuracy")}-->
<!--    <div class="text-[10px]">-->
<!--      {$_(-->
<!--        "Deals with at least one location with either accuracy level 'Coordinates' or 'Exact location' or at least one polygon.",-->
<!--      )}-->
<!--    </div>-->
<!--  </div>-->
<!--  <div class="flex flex-col items-center gap-2">-->
<!--    <div class="bg-neutral-200 p-3 font-bold drop-shadow-lg">-->
<!--      <div class="text-2xl">{counts.deals_public_polygons}</div>-->
<!--      <div>{getRatio(counts.deals_public_polygons)}</div>-->
<!--    </div>-->
<!--    {$_("Deals with polygon data")}-->
<!--    <div class="text-[10px]">&nbsp;</div>-->
<!--  </div>-->
<!--</div>-->
