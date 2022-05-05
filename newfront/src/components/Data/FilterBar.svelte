<script lang="ts">
  import { gql, request } from "graphql-request";
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import { GQLEndpoint } from "$lib";
  import { filters } from "$lib/filters";
  import { publicOnly } from "$lib/filters";
  import { countries, regions, user } from "$lib/stores";
  import { formfields } from "$lib/stores";
  import type { Investor } from "$lib/types/investor";
  import { isDefaultFilter, showFilterBar } from "$components/Data";
  import {
    implementation_status_choices,
    intention_of_investment_choices,
    nature_of_deal_choices,
  } from "$components/Fields/Display/choices";
  import FilterCollapse from "./FilterCollapse.svelte";
  import Wimpel from "./Wimpel.svelte";

  $: produce_choices = $formfields
    ? [
        {
          type: $_("Crop"),
          options: Object.entries($formfields.deal.crops.choices).map(([k, v]) => ({
            name: v,
            id: `crop_${k}`,
            value: k,
          })),
        },
        {
          type: $_("Livestock"),
          options: Object.entries($formfields.deal.animals.choices).map(([k, v]) => ({
            name: v,
            id: `animal_${k}`,
            value: k,
          })),
        },
        {
          type: $_("Minerals"),
          options: Object.entries($formfields.deal.mineral_resources.choices).map(
            ([k, v]) => ({ name: v, id: `mineral_${k}`, value: k })
          ),
        },
      ]
    : [];

  //   watch: {
  //     showFilterBar(state) {
  //       this.$emit("visibility-changed", state);
  //     },
  //   },
  $: console.log(produce_choices);

  $: countriesWithDeals = $countries.filter((c) => c.deals.length > 0);

  const choices = {
    implementation_status: {
      UNKNOWN: $_("No information"),
      ...implementation_status_choices,
    },
    nature_of_deal: nature_of_deal_choices,
    intention_of_investment: intention_of_investment_choices,
  };

  $: regionsWithGlobal = [
    {
      id: undefined,
      name: "Global",
    },
    ...$regions,
  ];

  let investors: Investor[] = [];
  async function getInvestors() {
    const query = gql`
      query Investors($limit: Int!, $subset: Subset) {
        investors(limit: $limit, subset: $subset) {
          id
          name
        }
      }
    `;
    const variables = {
      limit: 0,
      subset: $user?.is_authenticated ? "ACTIVE" : "PUBLIC",
    };
    const res = await request(GQLEndpoint, query, variables);
    investors = res.investors;
  }

  onMount(() => {
    getInvestors();
  });

  $: jsonFilters = JSON.stringify($filters.toGQLFilterArray());
  $: dataDownloadURL = `/api/legacy_export/?filters=${jsonFilters}&subset=${
    $publicOnly ? "PUBLIC" : "ACTIVE"
  }&format=`;

  function trackDownload(format) {
    let name = "Global";
    if ($filters.country_id) {
      name = $countries.find((c) => c.id === $filters.country_id).name;
    }
    if ($filters.region_id) {
      name = $regions.find((r) => r.id === $filters.region_id).name;
    }
    // noinspection TypeScriptUnresolvedVariable
    window._paq.push(["trackEvent", "Downloads", format, name]);
  }
</script>

<div
  class="absolute bg-white/90 top-0 left-0 bottom-0 z-10 flex text-sm drop-shadow-[3px_-3px_3px_rgba(0,0,0,0.3)] {$showFilterBar
    ? 'w-[clamp(220px,20%,300px)]'
    : 'w-0'}"
>
  <Wimpel
    showing={$showFilterBar}
    on:click={() => showFilterBar.set(!$showFilterBar)}
  />
  <div
    class="w-full h-full overflow-y-auto overflow-x-hidden p-2 flex flex-col"
    class:hidden={!$showFilterBar}
  >
    <div class="w-full self-start">
      <h3 class="mt-2 mb-1 text-black">{$_("Filter")}</h3>
      <span style="font-size: 0.8em">
        <label>
          <input type="checkbox" checked={$isDefaultFilter} />
          {$_("Default filter")}
        </label>
      </span>
      {#if $user?.bigrole}
        <!--v-if="$store.getters.userInGroup(['Administrators', 'Editors'])"-->
        <span style="font-size: 0.8em">
          <label>
            <input type="checkbox" checked={$publicOnly} />
            {$_("Public deals only")}
          </label>
        </span>
      {/if}

      <FilterCollapse
        title={$_("Land Matrix region")}
        clearable={!!$filters.region_id}
        on:click={() => ($filters.region_id = undefined)}
      >
        {#each regionsWithGlobal as reg}
          <label class="block">
            <input
              type="radio"
              bind:group={$filters.region_id}
              value={reg.id}
              on:change={() => ($filters.country_id = undefined)}
            />
            {$_(reg.name)}
          </label>
        {/each}
      </FilterCollapse>

      <FilterCollapse
        title={$_("Country")}
        clearable={!!$filters.country_id}
        on:click={() => ($filters.country_id = null)}
      >
        <select
          bind:value={$filters.country_id}
          class="inpt"
          on:change={() => ($filters.region_id = undefined)}
        >
          <option value={undefined} />
          {#each countriesWithDeals as c}
            <option value={c.id}>{c.name}</option>
          {/each}
        </select>
      </FilterCollapse>

      <FilterCollapse
        title={$_("Deal size")}
        clearable={!!($filters.deal_size_min || $filters.deal_size_max)}
        on:click={() => ($filters.deal_size_min = $filters.deal_size_max = undefined)}
      >
        <div class="field-has-appendix">
          <input
            bind:value={$filters.deal_size_min}
            type="number"
            class="inpt"
            placeholder={$_("from")}
            aria-label="from"
            max={$filters.deal_size_max}
          />
          <span>ha</span>
        </div>
        <div class="field-has-appendix">
          <input
            bind:value={$filters.deal_size_max}
            type="number"
            class="inpt"
            placeholder={$_("to")}
            aria-label="to"
            min={$filters.deal_size_min}
          />
          <span>ha</span>
        </div>
      </FilterCollapse>

      <!--        <FilterBarNegotiationStatusToggle />-->

      <FilterCollapse
        title={$_("Nature of the deal")}
        clearable={$filters.nature_of_deal.length > 0}
        on:click={() => ($filters.nature_of_deal = [])}
      >
        {#each Object.entries(choices.nature_of_deal) as [isval, isname]}
          <label class="block">
            <input type="checkbox" bind:group={$filters.nature_of_deal} value={isval} />
            {$_(isname)}
          </label>
        {/each}
      </FilterCollapse>

      <!--        <FilterCollapse-->
      <!--          :title="$_('Investor')"-->
      <!--          :clearable="!!(investor || investor_country)"-->
      <!--          @click="investor = investor_country = null"-->
      <!--        >-->
      <!--          <div>-->
      <!--            {{ $_("Investor name") }}-->
      <!--            <multi-select-->
      <!--              v-model="investor"-->
      <!--              :options="investors"-->
      <!--              :multiple="false"-->
      <!--              :close-on-select="true"-->
      <!--              placeholder="Investor"-->
      <!--              track-by="id"-->
      <!--              label="name"-->
      <!--              select-label=""-->
      <!--            />-->
      <!--            {{ $_("Country of registration") }}-->
      <!--            <multi-select-->
      <!--              v-model="investor_country"-->
      <!--              :options="countries"-->
      <!--              label="name"-->
      <!--              select-label=""-->
      <!--              placeholder="Country of registration"-->
      <!--            />-->
      <!--          </div>-->
      <!--        </FilterCollapse>-->

      <FilterCollapse
        title={$_("Year of initiation")}
        clearable={!!($filters.initiation_year_min || $filters.initiation_year_max)}
        on:click={() =>
          ($filters.initiation_year_min = $filters.initiation_year_max = undefined)}
      >
        <div class="flex">
          <input
            bind:value={$filters.initiation_year_min}
            type="number"
            class="inpt"
            placeholder="from"
            aria-label="from"
            min="1970"
            max={new Date().getFullYear()}
          />
          <input
            bind:value={$filters.initiation_year_max}
            type="number"
            class="inpt"
            placeholder="to"
            aria-label="to"
            min="1970"
            max={new Date().getFullYear()}
          />
        </div>

        <label class="block">
          <input
            id="initiation_year_unknown"
            bind:checked={$filters.initiation_year_unknown}
            type="checkbox"
            disabled={!$filters.initiation_year_min && !$filters.initiation_year_max}
          />

          {$_("Include unknown years")}
        </label>
      </FilterCollapse>

      <FilterCollapse
        title={$_("Implementation status")}
        clearable={$filters.implementation_status.length > 0}
        on:click={() => ($filters.implementation_status = [])}
      >
        {#each Object.entries(choices.implementation_status) as [isval, isname]}
          <label class="block">
            <input
              bind:group={$filters.implementation_status}
              class="form-check-input custom-control-input"
              type="checkbox"
              value={isval}
            />
            {$_(isname)}
          </label>
        {/each}
      </FilterCollapse>

      <FilterCollapse
        title={$_("Intention of investment")}
        clearable={$filters.intention_of_investment.length > 0}
        on:click={() => ($filters.intention_of_investment = [])}
      >
        <div class="hint p-1 mb-2 rounded bg-white text-xs italic">
          {$_(
            "Please note that excluding one intention of investment will exclude all deals that report the respective intention of investment, including deals that have other intentions of investments aside from the excluded one."
          )}
        </div>
        {#each Object.entries(choices.intention_of_investment) as [name, options]}
          <div>
            <strong>{$_(name)}</strong>
            {#each Object.entries(options) as [isval, isname]}
              <label class="block">
                <input
                  type="checkbox"
                  bind:group={$filters.intention_of_investment}
                  value={isval}
                />
                {$_(isname)}
              </label>
            {/each}
          </div>
        {/each}
      </FilterCollapse>

      <!--        <FilterCollapse-->
      <!--          :title="$_('Produce')"-->
      <!--          :clearable="produce.length > 0"-->
      <!--          @click="produce = []"-->
      <!--        >-->
      <!--          <multi-select-->
      <!--            v-model="produce"-->
      <!--            :options="produce_choices"-->
      <!--            :multiple="true"-->
      <!--            :close-on-select="false"-->
      <!--            placeholder="Produce"-->
      <!--            :group-select="true"-->
      <!--            group-label="type"-->
      <!--            group-values="options"-->
      <!--            track-by="id"-->
      <!--            label="name"-->
      <!--            select-label=""-->
      <!--          />-->
      <!--        </FilterCollapse>-->

      <FilterCollapse
        title={$_("Scope")}
        clearable={$filters.transnational !== null}
        on:click={() => ($filters.transnational = null)}
      >
        <label class="block">
          <input type="radio" bind:group={$filters.transnational} value={true} />
          {$_("Transnational")}
        </label>
        <label class="block">
          <input type="radio" bind:group={$filters.transnational} value={false} />
          {$_("Domestic")}
        </label>
      </FilterCollapse>

      <FilterCollapse
        title={$_("Forest concession")}
        clearable={$filters.forest_concession !== null}
        on:click={() => ($filters.forest_concession = null)}
      >
        <label class="block">
          <input type="radio" bind:group={$filters.forest_concession} value={null} />
          {$_("Included")}
        </label>
        <label class="block">
          <input type="radio" bind:group={$filters.forest_concession} value={false} />
          {$_("Excluded")}
        </label>
        <label class="block">
          <input type="radio" bind:group={$filters.forest_concession} value={true} />
          {$_("Only")}
        </label>
      </FilterCollapse>
    </div>
    <div class="self-end mt-auto pt-10 w-full">
      <slot />
      <FilterCollapse title={$_("Download")}>
        <ul>
          <li>
            <a href={dataDownloadURL + "xlsx"} on:click={() => trackDownload("xlsx")}>
              <i class="fas fa-file-download" />
              {$_("All attributes (xlsx)")}
            </a>
          </li>
          <li>
            <a href={dataDownloadURL + "csv"} on:click={() => trackDownload("csv")}>
              <i class="fas fa-file-download" />
              {$_("All attributes (csv)")}
            </a>
          </li>
          <li>
            <a
              href="/api/data.geojson?type=points&filters={jsonFilters}&subset={$publicOnly
                ? 'PUBLIC'
                : 'ACTIVE'}"
            >
              <i class="fas fa-file-download" />
              {$_("Locations (as geojson)")}
            </a>
          </li>
          <li>
            <a
              href="/api/data.geojson?type=areas&filters={jsonFilters}&subset={$publicOnly
                ? 'PUBLIC'
                : 'ACTIVE'}"
            >
              <i class="fas fa-file-download" />
              {$_("Areas (as geojson)")}
            </a>
          </li>
        </ul>
      </FilterCollapse>
    </div>
  </div>
</div>

<!--<style lang="scss">-->

<!--    .default-filter-switch {-->
<!--      &.active {-->
<!--        color: var(&#45;&#45;color-lm-orange);-->
<!--      }-->

<!--      label.custom-control-label {-->
<!--        font-size: 0.9rem;-->

<!--        &:hover {-->
<!--          cursor: pointer;-->
<!--        }-->

<!--        &:before {-->
<!--          font-size: 0.8rem;-->
<!--          background-color: rgba(black, 0.1);-->
<!--          border-width: 0;-->
<!--          width: 1.9em;-->
<!--          height: 0.65em;-->
<!--          margin-top: 0.2em;-->
<!--          margin-left: 0.15em;-->

<!--          &:focus {-->
<!--            outline: none;-->
<!--          }-->
<!--        }-->

<!--        &:after {-->
<!--          margin-top: -0.1em;-->
<!--          background-color: white;-->
<!--          box-shadow: 0 1px 2px rgba(black, 0.3);-->
<!--        }-->
<!--      }-->
<!--    }-->

<!--    .custom-switch .custom-control-input:checked ~ .custom-control-label {-->
<!--      &:before {-->
<!--        background-color: var(&#45;&#45;color-lm-orange-light-10);-->
<!--      }-->

<!--      &:after {-->
<!--        background-color: var(&#45;&#45;color-lm-orange);-->
<!--        box-shadow: 0 0 0 1px var(&#45;&#45;color-lm-orange-light);-->
<!--      }-->
<!--    }-->

<!--    .custom-control-input:focus ~ .custom-control-label {-->
<!--      &:before {-->
<!--        box-shadow: none;-->
<!--      }-->
<!--    }-->

<!--    .form-check {-->
<!--      padding: 0;-->

<!--      .custom-control.custom-checkbox {-->
<!--        min-height: 0;-->
<!--        padding-left: 1.3rem;-->

<!--        label.custom-control-label {-->
<!--          &:hover {-->
<!--            cursor: pointer;-->
<!--          }-->

<!--          line-height: 1.2;-->

<!--          &:before,-->
<!--          &:after {-->
<!--            top: 1px;-->
<!--            left: -1.3rem;-->
<!--          }-->
<!--        }-->
<!--      }-->

<!--      .custom-control-input:focus ~ .custom-control-label {-->
<!--        &:before {-->
<!--          border-color: #adb5bd;-->
<!--        }-->
<!--      }-->

<!--      .custom-control-input:checked ~ .custom-control-label {-->
<!--        &:before {-->
<!--          background-color: var(&#45;&#45;color-lm-orange-light);-->
<!--          border-color: transparent;-->
<!--        }-->
<!--      }-->

<!--      &:not(:first-child) {-->
<!--        .custom-control.custom-checkbox {-->
<!--          margin-top: 2px;-->
<!--        }-->
<!--      }-->
<!--    }-->
<!--  }-->
<!--</style>-->
