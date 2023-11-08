<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import NavDropDown from "$components/Navbar/NavDropDown.svelte"

  const showAllCharts = !!import.meta.env.VITE_FF_DISPLAY_ALL_CHARTS

  let dataViews: { title: string; route: string }[]
  $: dataViews = [
    {
      title: $_("Deals"),
      route: "/list/deals/",
    },
    {
      title: $_("Investors"),
      route: "/list/investors/",
    },
  ]

  let chartViews: { title: string; route: string }[] = []
  $: {
    chartViews = [
      {
        title: $_("Web of transnational deals"),
        route: "/charts/web-of-transnational-deals/",
      },
      {
        title: $_("Dynamics overview"),
        route: "/charts/dynamics-overview/",
      },
      {
        title: $_("Produce info map"),
        route: "/charts/produce-info/",
      },
    ]
    if (showAllCharts) {
      chartViews = [
        ...chartViews,
        {
          title: $_("Global map of Investments"),
          route: "/charts/global-map-of-investments/",
        },
      ]
    }
  }

  let countryProfileViews: { title: string; route: string }[] = []
  $: {
    countryProfileViews = [
      {
        title: $_("LSLA by negotiation status"),
        route: "/country-profile/lsla/",
      },
      {
        title: $_("Dynamics of deal by investor type"),
        route: "/country-profile/dynamics-of-deal/",
      },
      {
        title: $_("Number of intentions per category of production"),
        route: "/country-profile/intentions-of-investments/",
      },
      {
        title: $_("Concluded deals over time"),
        route: "/country-profile/concluded-deals-over-time/",
      },
    ]

    if (showAllCharts) {
      countryProfileViews = [
        {
          title: $_("Land acquisitions by category of production"),
          route: "/country-profile/land-acquisitions/",
        },
        ...countryProfileViews,
      ]
    }
  }
</script>

<div
  class="pointer-events-none absolute inset-x-0 top-3 z-30 mx-auto text-center drop-shadow"
>
  <nav id="data-navigation">
    <ul
      class="pointer-events-auto inline-flex items-center border border-orange bg-white text-left drop-shadow dark:bg-gray-800"
    >
      <li>
        <a
          href="/map/"
          class="nav-link"
          class:active={$page.url.pathname.startsWith("/map")}
        >
          {$_("Map")}
        </a>
      </li>
      <li>
        <NavDropDown>
          <svelte:fragment slot="title">
            <span class="capitalize">{$_("Data")}</span>
          </svelte:fragment>
          <ul class="border-2 border-orange bg-white dark:bg-gray-800">
            {#each dataViews as view}
              <li class="whitespace-nowrap">
                <a
                  href={view.route}
                  class="nav-link"
                  class:active={$page.url.pathname.startsWith(view.route)}
                >
                  {view.title}
                </a>
              </li>
            {/each}
          </ul>
        </NavDropDown>
      </li>
      <li>
        <NavDropDown>
          <svelte:fragment slot="title">
            <span class="capitalize">{$_("Charts")}</span>
          </svelte:fragment>
          <ul class="border-2 border-orange bg-white dark:bg-gray-800">
            <li
              class="whitespace-nowrap border-b border-b-orange bg-lm-dark px-4 py-1 font-bold text-white"
            >
              {$_("Charts")}
            </li>
            {#each chartViews as view}
              <li class="whitespace-nowrap">
                <a
                  href={view.route}
                  class="nav-link"
                  class:active={$page.url.pathname.startsWith(view.route)}
                >
                  {view.title}
                </a>
              </li>
            {/each}
            <li
              class="whitespace-nowrap border-y border-y-orange bg-lm-dark px-4 py-1 font-bold text-white"
            >
              {$_("Country profile charts")}
            </li>
            {#each countryProfileViews as view}
              <li class="whitespace-nowrap">
                <a
                  href={view.route}
                  class="nav-link"
                  class:active={$page.url.pathname.startsWith(view.route)}
                >
                  {view.title}
                </a>
              </li>
            {/each}
          </ul>
        </NavDropDown>
      </li>
    </ul>
  </nav>
</div>
