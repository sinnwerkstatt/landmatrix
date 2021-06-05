<template>
  <div>
    <table class="table table-condensed">
      <thead>
        <tr>
          <th>Created</th>
          <th v-if="$store.getters.userAuthenticated">User</th>
          <th>Fully updated</th>
          <th>Status</th>
          <th>Comment</th>
          <th style="text-align: right;">
            <!--            Show / <a @click="compareVersions">Compare</a>-->
            Show
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(version, i) in investor.versions" :key="i">
          <td>{{ version.revision.date_created | dayjs("YYYY-MM-DD HH:mm") }}</td>
          <td v-if="$store.getters.userAuthenticated">
            {{ version.revision.user && version.revision.user.full_name }}
          </td>
          <td>
            <b-button
              v-b-tooltip.hover
              disabled
              :title="version.investor.fully_updated ? 'Fully updated' : 'Updated'"
              :class="[
                'fa',
                version.investor.fully_updated ? 'fa-check-circle' : 'fa-circle',
              ]"
            />
          </td>
          <td>
            {{ version.investor.status }}
          </td>
          <td>{{ version.revision.comment }}</td>
          <td style="white-space: nowrap; text-align: right;">
            <span v-if="i === deduced_position">Current</span>
            <span v-else>
              <router-link
                v-slot="{ href }"
                :to="{
                  name: 'investor_detail',
                  params: { investorId, investorVersion: version.revision.id },
                }"
              >
                <!-- this hack helps to understand that a new version is actually loading, atm -->
                <a :href="href">Show</a>
              </router-link>
            </span>
            <!--            <span class="ml-4" style="white-space: nowrap; text-align: right;">-->
            <!--              <input-->
            <!--                type="radio"-->
            <!--                v-model="compare_from"-->
            <!--                :value="version.revision.id"-->
            <!--                :disabled="version.revision.id >= compare_to"-->
            <!--              />-->

            <!--              <input-->
            <!--                type="radio"-->
            <!--                v-model="compare_to"-->
            <!--                :value="version.revision.id"-->
            <!--                :disabled="version.revision.id <= compare_from"-->
            <!--              />-->
            <!--            </span>-->
          </td>
        </tr>
      </tbody>
      <!--      <tfoot>-->
      <!--        <tr>-->
      <!--          <td></td>-->
      <!--          <td></td>-->
      <!--          <td></td>-->
      <!--          <td></td>-->
      <!--          <td></td>-->
      <!--          <td>-->
      <!--            <button style="white-space: nowrap;" @click="compareVersions">-->
      <!--              Compare versions-->
      <!--            </button>-->
      <!--          </td>-->
      <!--        </tr>-->
      <!--      </tfoot>-->
    </table>
  </div>
</template>

<script>
  import { draft_status_map, status_map } from "$utils/choices";

  export default {
    name: "InvestorHistory",
    props: ["investor", "investorId", "investorVersion"],
    data() {
      return {
        compare_from: null,
        compare_to: null,
      };
    },
    computed: {
      deduced_position() {
        if (this.investor.versions.length === 0) return 0;
        if (this.investorVersion) {
          return this.investor.versions.findIndex(
            (v) => +v.revision.id === +this.investorVersion
          );
        }
        for (const [i, v] of this.investor.versions.entries()) {
          if (v.investor.draft_status === null) return i;
        }
        return this.investor.versions.length - 1;
      },
    },
    mounted() {
      if (this.investor.versions.length >= 2) {
        this.compare_to = this.investor.versions[0].revision.id;
        this.compare_from = this.investor.versions[1].revision.id;
      }
    },
    methods: {
      derive_status(status, draft_status) {
        if (draft_status) {
          return draft_status_map[draft_status];
        }
        let st = status_map[status];
        if (draft_status) {
          return `${st} + ${draft_status_map[draft_status]}`;
        }
        return st;
      },
      compareVersions() {
        this.$router.push({
          name: "investor_compare",
          params: {
            investorId: this.investorId,
            fromVersion: this.compare_from,
            toVersion: this.compare_to,
          },
        });
      },
    },
  };
</script>
