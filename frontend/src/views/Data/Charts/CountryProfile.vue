<template>
  <ChartsContainer>
    <div class="country-profile-graph">
      <h2>
        Number of intentions per category of production according to implementation
        status
      </h2>
      <div class="sankey-wrapper">
        <LoadingPulse v-if="$apollo.loading" />
        <svg id="sankey" />
      </div>
      <div class="download-buttons">
        <button class="btn" @click="downloadImage('svg')">
          <i class="fas fa-file-image" /> SVG
        </button>
        <span id="download-png">
          <button
            class="btn"
            :class="{ 'use-chrome': !isChrome }"
            @click="downloadImage('png')"
          >
            <i class="fas fa-file-image" />
            PNG
          </button>
        </span>
        <b-tooltip v-if="!isChrome" target="download-png" triggers="hover">
          At the moment, downloading PNG does not work in Firefox.
        </b-tooltip>
        <span id="download-webp">
          <button
            class="btn"
            :class="{ 'use-chrome': !isChrome }"
            @click="downloadImage('webp')"
          >
            <i class="fas fa-file-image" /> WebP
          </button>
        </span>
        <b-tooltip v-if="!isChrome" target="download-webp" triggers="hover">
          At the moment, downloading WebP does not work in Firefox.
        </b-tooltip>
        <span style="margin: 2rem 0">|</span>
        <button class="btn" @click="downloadJSON">
          <i class="fas fa-file-code" /> JSON
        </button>
        <button class="btn" @click="downloadCSV">
          <i class="fas fa-file-code" /> CSV
        </button>
      </div>
      <div class="legend">
        {{
          $t("This figure lists the intention of investments per negotiation status.")
        }}
        <br />
        {{ $t("Please note: a deal may have more than one intention.") }}<br />
        <i v-if="sankey_legend_numbers"
          >{{
            $t(
              "{x} deals have multiple intentions, resulting in a total of {y} intentions for {z} deals.",
              sankey_legend_numbers
            )
          }}
        </i>
      </div>
    </div>
  </ChartsContainer>
</template>

<script>
  import LoadingPulse from "$components/Data/LoadingPulse";
  import { a_download, chart_download } from "$utils/charts";
  import {
    flat_intention_of_investment_map,
    implementation_status_choices,
  } from "$utils/choices";
  import ChartsContainer from "$views/Data/Charts/ChartsContainer";
  import {
    LamaSankey,
    sankey_links_to_csv_cross,
  } from "$views/Data/Charts/country_profile_sankey";
  import { data_deal_query } from "$views/Data/query";

  export default {
    name: "CountryProfileGraphs",
    components: { LoadingPulse, ChartsContainer },
    metaInfo() {
      return { title: this.$t("Country profile graphs") };
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => vm.$store.dispatch("showContextBar", false));
    },
    data() {
      return { deals: null, sankey: null, sankey_links: null };
    },
    apollo: {
      deals: data_deal_query,
    },
    computed: {
      sankey_legend_numbers() {
        if (!this.deals) return null;
        let multi_deal_count = this.deals.filter(
          (d) => d.current_intention_of_investment?.length > 1
        ).length;
        let all_intentions = this.deals
          .map((d) => d.current_intention_of_investment?.length || 0)
          .reduce((a, b) => a + b, 0);
        return { x: multi_deal_count, y: all_intentions, z: this.deals.length };
      },
      isChrome() {
        return /Google Inc/.test(navigator.vendor);
      },
    },
    watch: {
      deals() {
        if (!this.deals) return;
        let datanodes = new Set();
        let datalinks = {};

        let i_status_counter = {};

        this.deals.forEach((d) => {
          if (!d.current_implementation_status)
            d.current_implementation_status = "S_UNKNOWN";
          if (!d.current_intention_of_investment)
            d.current_intention_of_investment = ["I_UNKNOWN"];
          datanodes.add(d.current_implementation_status);
          i_status_counter[d.current_implementation_status] =
            i_status_counter[d.current_implementation_status] + 1 || 1;

          d.current_intention_of_investment?.forEach((ivi) => {
            datanodes.add(ivi);
            datalinks[[d.current_implementation_status, ivi]] =
              datalinks[[d.current_implementation_status, ivi]] + 1 || 1;
          });
        });

        const nodes = [...datanodes].map((n) => {
          let istatus = implementation_status_choices[n] || n === "S_UNKNOWN";
          return {
            id: n,
            istatus,
            deal_count: istatus ? i_status_counter[n] : 0,
            name:
              (n === "S_UNKNOWN" && this.$t("Status unknown")) ||
              (n === "I_UNKNOWN" && this.$t("Intention unknown")) ||
              implementation_status_choices[n] ||
              flat_intention_of_investment_map[n],
          };
        });

        const links = Object.entries(datalinks).map(([k, v]) => {
          let [source, target] = k.split(",");
          return { source, target, value: v };
        });
        this.sankey_links = JSON.parse(JSON.stringify(links));
        this.sankey.do_the_sank({ nodes, links });
      },
    },
    mounted() {
      this.sankey = new LamaSankey("#sankey");
    },
    methods: {
      _fileName(suffix = "") {
        let filters = this.$store.state.filters.filters;
        let prefix = "Global - ";
        if (filters.country_id)
          prefix =
            this.$store.getters.getCountryOrRegion({
              type: "country",
              id: filters.country_id,
            }).name + " - ";
        if (filters.region_id)
          prefix =
            this.$store.getters.getCountryOrRegion({
              type: "region",
              id: filters.region_id,
            }).name + " - ";
        return (
          prefix +
          this.$t(
            "Number of intentions per category of production according to implementation status"
          ) +
          suffix
        );
      },
      downloadImage(filetype) {
        chart_download(
          document.querySelector("#sankey"),
          `image/${filetype}`,
          this._fileName(`.${filetype}`)
        );
      },
      downloadJSON() {
        let data =
          "data:application/json;charset=utf-8," +
          encodeURIComponent(JSON.stringify(this.sankey_links, null, 2));
        a_download(data, this._fileName(".json"));
      },
      downloadCSV() {
        console.log(this.sankey_links);
        let csv = sankey_links_to_csv_cross(this.sankey_links);
        let data = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
        a_download(data, this._fileName(".csv"));
        // this.sankey_links;
        // encodeURIComponent();
      },
    },
  };
</script>
<style lang="scss" scoped>
  .country-profile-graph {
    max-height: 80vh;
    margin: 5rem 3rem;
    background: var(--color-lm-orange-light-10);
    border-radius: 1rem;
    padding: 1rem;
    display: flex;
    flex-flow: column wrap;
  }
  .sankey-wrapper {
    flex-grow: 1;
    max-width: 100%;
    border-radius: 5px 5px 0 0;
  }
  .download-buttons {
    background: #2d2d2dff;
    color: var(--color-lm-light);
    border-radius: 0 0 5px 5px;

    button {
      color: var(--color-lm-light);
      font-size: 0.85rem;
      padding: 0 0.75rem 0.15rem;
    }
  }
</style>

<style lang="scss">
  .sankey-wrapper {
    background: white;
    .link:hover {
      stroke-opacity: 0.9;
    }
  }
  .use-chrome {
    opacity: 0.7;
    pointer-events: none;
  }
</style>
