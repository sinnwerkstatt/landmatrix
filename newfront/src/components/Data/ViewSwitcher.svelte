<script lang="ts">
  import { _ } from "svelte-i18n";
  // if (this.$route.name === "list_deals") {
  //   return this.label.deals;
  // } else if (this.$route.name === "list_investors") {
  //   return this.label.investors;
  // } else {
  //   return $_("Table");
  // }
  // }
  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte";
  import DropDown from "../LowLevel/DropDown.svelte";

  const label = { deals: $_("Deals"), investors: $_("Investors") };
  const chartEntries = [
    {
      title: $_("Web of transnational deals"),
      route: "/charts/web-of-transnational-deals",
    },
    {
      title: $_("Dynamics overview"),
      route: "/charts/dynamics-overview",
    },
    {
      title: $_("Produce info map"),
      route: "/charts/produce-info",
    },
    {
      title: $_("Country profiles"),
      route: "/charts/country-profiles",
    },
  ];

  // $: isListRoute = return ["list_deals", "list_investors"].includes($route.name);

  let isListRoute = false;
  let isChartRoute = false;
  // let isChartRoute() {
  //   return this.chartEntries.map((e) => e.route_name).includes(this.$route.name);

  $: dataItemName = {};
</script>

<div class="absolute mx-auto top-3 inset-x-0 text-center z-30 drop-shadow">
  <nav>
    <ul class="inline-flex drop-shadow">
      <li class="bg-white px-4 py-1">
        <a href="/map" class="text-black">
          {$_("Map")}
        </a>
      </li>
      <li class="bg-white px-4 py-1">
        <DropDown>
          <div slot="button" class="flex items-center gap-2 hover:text-orange">
            {$_("Table")}
            <ChevronDownIcon class="h-3 w-3" />
          </div>
          <div class="bg-white border-orange-50 p-2 text-left">
            <div class="bg-white border-orange-50 p-2 text-left">
              {#if dataItemName !== label.deals}
                <a href="/deals" class="block">
                  {label.deals}
                </a>
              {/if}
              {#if dataItemName !== label.investors}
                <a href="/investors" class="block">
                  {label.investors}
                </a>
              {/if}
            </div>
          </div>
        </DropDown>
      </li>

      <li class="bg-white px-4 py-1">
        <DropDown>
          <div slot="button" class="flex items-center gap-2 hover:text-orange">
            {$_("Charts")}
            <ChevronDownIcon class="h-3 w-3" />
          </div>
          <div class="bg-white border-orange-50 p-2 text-left">
            <div class="bg-white border-orange-50 p-2 text-left">
              <div class="bg-white border-orange-50 p-2 text-left">
                {#each chartEntries as entry}
                  <a href={entry.route} class="block">
                    {entry.title}
                  </a>
                {/each}
                <div id="arrow" data-popper-arrow />
              </div>
            </div>
          </div>
        </DropDown>
      </li>
    </ul>
  </nav>
</div>
