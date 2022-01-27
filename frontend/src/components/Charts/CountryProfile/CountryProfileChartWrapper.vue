<template>
  <div class="country-profile-chart-wrapper">
    <slot name="heading">
      <h2>{{ title }}</h2>
    </slot>
    <div class="svg-wrapper">
      <slot name="default"></slot>
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
      <button class="btn" @click="$emit('downloadJSON')">
        <i class="fas fa-file-code" /> JSON
      </button>
      <button class="btn" @click="$emit('downloadCSV')">
        <i class="fas fa-file-code" /> CSV
      </button>
    </div>
    <div class="legend">
      <slot name="legend" />
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";
  import { data_deal_query } from "$views/Data/query";
  import { chart_download, fileName } from "$utils/charts";
  import type { Deal } from "$types/deal";

  export default Vue.extend({
    name: "CountryProfileChartWrapper",
    components: {},
    props: {
      svgId: { type: String, required: true },
      title: { type: String, required: true },
    },
    data() {
      return { deals: [] as Deal[] };
    },
    apollo: { deals: data_deal_query },
    computed: {
      isChrome(): boolean {
        return /Google Inc/.test(navigator.vendor);
      },
    },
    methods: {
      downloadImage(filetype: string) {
        chart_download(
          document.getElementById(this.svgId),
          `image/${filetype}`,
          fileName(this.title, `.${filetype}`)
        );
      },
    },
  });
</script>

<style lang="scss" scoped>
  .country-profile-chart-wrapper {
    min-height: 75vh;
    margin: 1rem 3rem 1rem;
    background: var(--color-lm-orange-light-10);
    border-radius: 1rem;
    padding: 1rem;
    display: flex;
    flex-flow: column nowrap;
  }
  h2 {
    font-size: 1.2rem;
  }
  .svg-wrapper {
    flex: 1 1 auto;
    max-width: 100%;
    border-radius: 5px 5px 0 0;
    background: white;
    display: flex;
    justify-content: center;
    align-items: center;
    * > {
      flex: 1 1 auto;
    }
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
  .legend {
    flex-shrink: 0;
    padding: 0.4rem;
  }
  .use-chrome {
    opacity: 0.7;
    pointer-events: none;
  }
</style>
