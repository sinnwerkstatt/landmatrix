<template>
  <div v-if="deal" class="w-screen max-w-screen">
    <h2 class="my-6 text-xl text-green-700 font-bold">Deal #{{ deal.id }}</h2>
    <button @click="checkAll(true)">Expand all</button> /
    <button @click="checkAll(false)">Hide all</button>
    <div class="p-3 flex flex-row divide-x divide-black">
      <div v-for="v in enriched_versions" :key="v.id" class="flex flex-col w-1/3 p-2">
        <input
          :id="`flop-${v.id}`"
          type="checkbox"
          class="flopmenu"
          :checked="v.showEntry"
        />
        <label :for="`flop-${v.id}`" />
        <div class="w-26 flex-shrink-0">
          <router-link
            class="text-blue-400"
            :to="{
              name: 'deal_detail',
              params: { dealId: dealId, dealVersion: v.id },
            }"
            >{{ v.id }}</router-link
          ><br />
          {{ dayjs(v.created_at).format("YYYY-MM-DD") }}<br />
          {{ combined_status_fn(v.deal.status, v.deal.draft_status) }}
        </div>

        <div
          v-for="ds in v.deal.datasources"
          :key="ds.id"
          class="flex-shrink overflow-hidden"
        >
          <div
            class="p-2 m-2 d-flex flex-column overflow-hidden rounded-lg"
            :class="[ds.file_is_probably_broken ? 'bg-yellow-300' : 'bg-green-200']"
          >
            <div>id: {{ ds.id }}</div>
            <div>type: {{ ds.type }}</div>
            <div class="whitespace-nowrap">url: {{ ds.url }}</div>
            <div>date: {{ ds.date }}</div>
            <div>name: {{ ds.name }}</div>
            <div>company: {{ ds.company }}</div>
            <div class="whitespace-nowrap">
              <div :class="{ probably_broken: ds.file_is_probably_broken }">
                file: {{ ds.file && ds.file.replace("uploads/", "") }}
              </div>
              <div v-if="ds.file_prop">
                replace: {{ ds.file_prop.replace("uploads/", "") }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";
  import type { DataSource, Deal, DealVersion } from "$types/deal";
  import gql from "graphql-tag";
  import dayjs from "dayjs";
  import { combined_status_fn } from "$utils/choices";

  interface EDealVersion extends DealVersion {
    showEntry?: boolean;
  }

  export default Vue.extend({
    props: {
      dealId: { type: [Number, String], required: true },
    },
    data() {
      return {
        deal: undefined as unknown as Deal,
      };
    },
    apollo: {
      deal: {
        query: gql`
          query ($id: Int!, $subset: Subset) {
            deal(id: $id, subset: $subset) {
              id

              versions {
                id
                deal {
                  fully_updated
                  status
                  draft_status
                  datasources
                }
                created_at
                created_by {
                  id
                  full_name
                }
                object_id
              }
            }
          }
        `,
        variables() {
          return {
            id: +this.dealId,
            subset: "UNFILTERED",
          };
        },
        fetchPolicy: "no-cache",
      },
    },
    computed: {
      enriched_versions(): EDealVersion[] {
        let ret = [] as EDealVersion[];
        let prev_dses = [] as DataSource[];
        let startflagging = false;
        this.deal.versions
          .slice()
          .reverse()
          .forEach((dv: EDealVersion) => {
            const dses = dv.deal.datasources as DataSource[];
            if (startflagging) {
              dv.showEntry = true;
            }
            if (prev_dses.length > dses.length) {
              startflagging = true;
              dv.showEntry = true;
              ret.at(-1).showEntry = true;

              // try to map the entries
              for (let [index, ds] of dses.entries()) {
                const pds = prev_dses[index];
                if (
                  ds.type === pds.type &&
                  ds.url === pds.url &&
                  ds.date === pds.date
                ) {
                  // this is fine
                } else {
                  const pds2 = prev_dses[index + 1];
                  ds.file_is_probably_broken = true;
                  ds.file_prop = pds2.file;
                  console.log({ index, ds, pds });
                }
              }
            }

            ret.push({ ...dv });
            prev_dses = dses;
          });
        return ret;
      },
    },
    methods: {
      dayjs,
      combined_status_fn,
      checkAll(arg: boolean) {
        let flops = document.querySelectorAll(".flopmenu");
        flops.forEach((e: Element) => ((e as HTMLInputElement).checked = arg));
      },
    },
  });
</script>

<style scoped>
  @import "../../static/tailwind.min.css";

  .probably_broken {
    color: red;
    font-weight: bold;
  }
  .flopmenu {
    visibility: hidden;
  }
  .flopmenu ~ div {
    width: 1rem;
    transition: width 50ms ease;
  }

  .flopmenu:checked ~ div {
    width: 100%;
  }
  .flopmenu + label::before {
    content: "SHOW";
    background: red;
  }

  .flopmenu:checked + label::before {
    content: "HIDE";
    background: green;
  }
</style>
