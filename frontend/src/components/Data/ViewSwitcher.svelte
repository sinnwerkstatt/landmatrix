<script lang="ts">
  import { env } from "$env/dynamic/public"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import NavDropDown from "$components/Navbar/NavDropDown.svelte"

  const showAllCharts = !!env.PUBLIC_FF_DISPLAY_ALL_CHARTS

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
    <ul class="pointer-events-auto inline-flex items-center text-left drop-shadow">
      <li>
        <a
          href="/map/"
          class="btn btn-flat rounded-r-none"
          class:btn-black={!$page.url.pathname.startsWith("/map")}
          class:btn-primary={$page.url.pathname.startsWith("/map")}
        >
          {$_("Map")}
        </a>
      </li>
      <li>
        <NavDropDown>
          <svelte:fragment slot="title">
            <span
              class="btn btn-flat rounded-none"
              class:btn-black={!$page.url.pathname.startsWith("/list")}
              class:btn-primary={$page.url.pathname.startsWith("/list")}
            >
              {$_("Tables")}
            </span>
          </svelte:fragment>

          <ul class="border-2 border-orange-500">
            {#each dataViews as view}
              <li class="whitespace-nowrap">
                <a
                  href={view.route}
                  class="btn btn-flat w-full rounded-none text-left"
                  class:btn-black={!$page.url.pathname.startsWith(view.route)}
                  class:btn-primary={$page.url.pathname.startsWith(view.route)}
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
            <span
              class="btn btn-flat btn-black rounded-l-none"
              class:btn-black={!["/charts", "/country-profile"].some(path =>
                $page.url.pathname.startsWith(path),
              )}
              class:btn-primary={["/charts", "/country-profile"].some(path =>
                $page.url.pathname.startsWith(path),
              )}
            >
              {$_("Charts")}
            </span>
          </svelte:fragment>
          <ul class="border-2 border-orange bg-white dark:bg-gray-800">
            {#each chartViews as view}
              <li class="whitespace-nowrap">
                <a
                  href={view.route}
                  class="btn btn-flat w-full rounded-none text-left"
                  class:btn-black={!$page.url.pathname.startsWith(view.route)}
                  class:btn-primary={$page.url.pathname.startsWith(view.route)}
                >
                  {view.title}
                </a>
              </li>
            {/each}
            {#each countryProfileViews as view}
              <li class="whitespace-nowrap">
                <a
                  href={view.route}
                  class="btn btn-flat w-full rounded-none text-left"
                  class:btn-black={!$page.url.pathname.startsWith(view.route)}
                  class:btn-primary={$page.url.pathname.startsWith(view.route)}
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
