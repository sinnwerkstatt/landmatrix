<template>
  <div>
    <h3>{{ $t("Deal history") }}</h3>
    <table class="table table-condensed">
      <thead>
        <tr>
          <th>{{ $t("Created") }}</th>
          <th v-if="$store.getters.userAuthenticated">{{ $t("User") }}</th>
          <th>{{ $t("Fully updated") }}</th>
          <th v-if="$store.getters.userAuthenticated">{{ $t("Status") }}</th>
          <th style="text-align: right">
            {{ $t("Show") }} / <a @click="compareVersions">{{ $t("Compare") }}</a>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(version, i) in enriched_versions" :key="i">
          <td>{{ version.created_at | dayjs("YYYY-MM-DD HH:mm") }}</td>
          <td v-if="$store.getters.userAuthenticated">
            {{ version.created_by && version.created_by.full_name }}
          </td>
          <td>
            <b-button
              v-b-tooltip.hover
              disabled
              :title="version.deal.fully_updated ? 'Fully updated' : 'Updated'"
              :class="[
                'fa',
                version.deal.fully_updated ? 'fa-check-circle' : 'fa-circle',
              ]"
            />
          </td>
          <td v-if="$store.getters.userAuthenticated">
            {{ $t(derive_status(version.deal.status, version.deal.draft_status)) }}
          </td>
          <td style="white-space: nowrap; text-align: right">
            <span v-if="i === deduced_position">{{ $t("Current") }}</span>
            <span v-else>
              <router-link v-slot="{ href }" :to="version.link">
                <!-- this hack helps to understand that a new version is actually loading, atm -->
                <a :href="href">{{ $t("Show") }}</a>
              </router-link>
            </span>
            <span class="ml-4" style="white-space: nowrap; text-align: right">
              <input
                v-model="compare_from"
                type="radio"
                :value="version.id"
                :disabled="version.id >= compare_to"
              />

              <input
                v-model="compare_to"
                type="radio"
                :value="version.id"
                :disabled="version.id <= compare_from"
              />
            </span>
          </td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <td></td>
          <td v-if="$store.getters.userAuthenticated"></td>
          <td></td>
          <td v-if="$store.getters.userAuthenticated"></td>
          <td v-if="compare_from && compare_to">
            <router-link
              :to="{
                name: 'deal_compare',
                params: {
                  dealId: dealId,
                  fromVersion: compare_from,
                  toVersion: compare_to,
                },
              }"
              class="btn btn-primary text-nowrap"
            >
              {{ $t("Compare versions") }}
            </router-link>
          </td>
        </tr>
      </tfoot>
    </table>
  </div>
</template>

<script lang="ts">
  import { draft_status_map, status_map } from "$utils/choices";
  import Vue from "vue";

  export default Vue.extend({
    name: "DealHistory",
    props: {
      deal: { type: Object, required: true },
      dealId: { type: [Number, String], required: true },
      dealVersion: { type: [Number, String], default: null },
    },
    data() {
      return {
        compare_from: null,
        compare_to: null,
      };
    },
    computed: {
      enriched_versions() {
        let current_active = false;
        let versions = this.deal.versions;
        if (!this.$store.getters.userAuthenticated) {
          versions = versions.filter(
            (v) => !(v.deal.confidential || v.deal.draft_status)
          );
        }
        return versions.map((v) => {
          if (!v.deal.draft_status && !current_active) {
            v.link = { name: "deal_detail", params: { dealId: this.dealId } };
            current_active = true;
          } else
            v.link = {
              name: "deal_detail",
              params: { dealId: this.dealId, dealVersion: v.id },
            };
          return v;
        });
      },
      deduced_position() {
        if (this.deal.versions.length === 0) return 0;
        if (this.dealVersion) {
          return this.deal.versions.findIndex((v) => +v.id === +this.dealVersion);
        }
        for (const [i, v] of this.deal.versions.entries()) {
          if (v.deal.draft_status === null) return i;
        }
        return this.deal.versions.length - 1;
      },
    },
    mounted() {
      if (this.deal.versions.length >= 2) {
        this.compare_to = this.deal.versions[0].id;
        this.compare_from = this.deal.versions[1].id;
      }
    },
    methods: {
      derive_status(status, draft_status) {
        return draft_status ? draft_status_map[draft_status] : status_map[status];
      },
      compareVersions() {
        this.$router.push({
          name: "deal_compare",
          params: {
            dealId: this.dealId,
            fromVersion: this.compare_from,
            toVersion: this.compare_to,
          },
        });
      },
    },
  });
</script>
