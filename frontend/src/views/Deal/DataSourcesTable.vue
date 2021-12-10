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
          <span class="whitespace-nowrap">{{
            dayjs(v.created_at).format("YYYY-MM-DD")
          }}</span
          ><br />
          <router-link
            class="text-blue-400"
            :to="{
              name: 'deal_detail',
              params: { dealId: dealId, dealVersion: v.id },
            }"
            >{{ v.id }}</router-link
          ><br />
          {{ combined_status_fn(v.deal.status, v.deal.draft_status) }}
        </div>

        <div
          v-for="ds in v.deal.datasources"
          :key="ds.id"
          class="flex-shrink overflow-hidden"
        >
          <div
            class="p-2 m-2 d-flex flex-column overflow-hidden rounded-lg h-64"
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
                file:
                <a :href="`${media_url}${ds.file}`">
                  {{ ds.file && ds.file.replace("uploads/", "") }}
                </a>
              </div>
              <div v-if="ds.file_prop">
                replace:
                <a :href="`${media_url}${ds.file_prop}`">
                  {{ ds.file_prop.replace("uploads/", "") }}
                </a>
              </div>
              <div>{{ ds.old_group_id }}</div>
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
        media_url: import.meta.env.VITE_MEDIA_URL,
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
        let prev_dv: EDealVersion;
        let prev_dv_shown = false;
        this.deal.versions
          .slice()
          .reverse()
          .forEach((dv: EDealVersion) => {
            const dses = dv.deal.datasources as DataSource[];
            if (startflagging) {
              dv.showEntry = true;
            }
            // if (prev_dses.length > dses.length) {
            //   startflagging = true;
            //   dv.showEntry = true;
            //   // ret.at(-1).showEntry = true;
            //
            //   // // try to map the entries
            //   // for (let [index, ds] of dses.entries()) {
            //   //   const pds = prev_dses[index];
            //   //   if (
            //   //     ds.type === pds.type &&
            //   //     ds.url === pds.url &&
            //   //     ds.date === pds.date
            //   //   ) {
            //   //     // this is fine
            //   //   } else {
            //   //     const pds2 = prev_dses[index + 1];
            //   //     ds.file_is_probably_broken = true;
            //   //     ds.file_prop = pds2.file;
            //   //     console.log({ index, ds, pds });
            //   //   }
            //   // }
            // }

            if (new Date(dv.created_at).getTime() >= new Date(2018, 1, 1).getTime()) {
              if (prev_dses.length > dses.length) {
                startflagging = true;
                dv.showEntry = true;
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
              if (prev_dv && !prev_dv_shown) {
                ret.push({ ...prev_dv });
                prev_dv_shown = true;
              }
              ret.push({ ...dv });
            }

            prev_dv = dv;
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
    border-radius: 5px;

    padding: 0.3em 0.75em;
    background: red;
  }

  .flopmenu:checked + label::before {
    content: "HIDE";
    border-radius: 5px;
    padding: 0.3em 0.75em;
    background: green;
    color: white;
  }
</style>
