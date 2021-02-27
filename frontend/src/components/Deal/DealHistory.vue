<template>
  <div>
    <h3>{{ $t("Deal History") }}</h3>
    <table class="table table-condensed">
      <thead>
        <tr>
          <th>{{ $t("Created") }}</th>
          <th v-if="$store.getters.userAuthenticated">{{ $t("User") }}</th>
          <th>{{ $t("Fully updated") }}</th>
          <th>{{ $t("Status") }}</th>
          <th>{{ $t("Comment") }}</th>
          <th style="text-align: right;">
            {{ $t("Show") }} / <a @click="compareVersions">{{ $t("Compare") }}</a>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(version, i) in deal.versions" :key="i">
          <td>{{ version.revision.date_created | defaultdate }}</td>
          <td v-if="$store.getters.userAuthenticated">
            {{ version.revision.user && version.revision.user.full_name }}
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
          <td>
            {{ $t(derive_status(version.deal.status, version.deal.draft_status)) }}
          </td>
          <td>{{ version.revision.comment }}</td>
          <td style="white-space: nowrap; text-align: right;">
            <span v-if="i === deduced_position">{{ $t("Current") }}</span>
            <span v-else>
              <router-link
                v-slot="{ href }"
                :to="{
                  name: 'deal_detail',
                  params: { dealId, dealVersion: version.revision.id },
                }"
              >
                <!-- this hack helps to understand that a new version is actually loading, atm -->
                <a :href="href">{{ $t("Show") }}</a>
              </router-link>
            </span>
            <span class="ml-4" style="white-space: nowrap; text-align: right;">
              <input
                v-model="compare_from"
                type="radio"
                :value="version.revision.id"
                :disabled="version.revision.id >= compare_to"
              />

              <input
                v-model="compare_to"
                type="radio"
                :value="version.revision.id"
                :disabled="version.revision.id <= compare_from"
              />
            </span>
          </td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td>
            <button
              class="btn btn-primary"
              style="white-space: nowrap;"
              @click="compareVersions"
            >
              {{ $t("Compare versions") }}
            </button>
          </td>
        </tr>
      </tfoot>
    </table>
  </div>
</template>

<script>
  export default {
    name: "DealHistory",
    props: ["deal", "dealId", "dealVersion"],
    data() {
      return {
        compare_from: null,
        compare_to: null,
      };
    },
    computed: {
      deduced_position() {
        if (this.deal.versions.length === 0) return 0;
        if (this.dealVersion) {
          return this.deal.versions.findIndex(
            (v) => +v.revision.id === +this.dealVersion
          );
        }
        for (const [i, v] of this.deal.versions.entries()) {
          if (v.deal.draft_status === null) return i;
        }
        return this.deal.versions.length - 1;
      },
    },
    mounted() {
      if (this.deal.versions.length >= 2) {
        this.compare_to = this.deal.versions[0].revision.id;
        this.compare_from = this.deal.versions[1].revision.id;
      }
    },
    methods: {
      derive_status(status, draft_status) {
        const status_map = {
          1: "Draft",
          2: "Live",
          3: "Updated",
          4: "Deleted",
        };
        const draft_status_map = {
          1: "Draft",
          2: "Review",
          3: "Activation",
          4: "Rejected",
          5: "To Delete",
        };

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
  };
</script>
