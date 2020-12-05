<template>
  <div>
    <h3>History</h3>
    <table class="table table-condensed">
      <tbody>
        <tr v-for="(version, i) in deal.versions">
          <td>{{ version.revision.date_created | defaultdate }}</td>
          <td v-if="user && user.is_authenticated">
            {{ version.revision.user && version.revision.user.full_name }}
          </td>
          <td>
            <b-button
              disabled
              v-b-tooltip.hover
              :title="version.deal.fully_updated ? 'Fully updated' : 'Updated'"
              :class="[
                'fa',
                version.deal.fully_updated ? 'fa-check-circle' : 'fa-circle',
              ]"
            />
          </td>
          <td>
            {{ derive_status(version.deal.status, version.deal.draft_status) }}
          </td>
          <td>{{ version.revision.comment }}</td>
          <td>
            <span v-if="i === deduced_position">Current</span>
            <router-link
              v-if="i !== deduced_position"
              :to="{
                name: 'deal_detail',
                params: { deal_id, deal_version: version.revision.id },
              }"
              v-slot="{ href, navigate }"
            >
              <!-- this hack helps to understand that a new version is actually loading, atm -->
              <a :href="href">Show</a>
            </router-link>
          </td>
          <td>
            <span :href="`/newdeal/deal/compare/${version.revision.id}/`">
              Compare with previous<br />not working yet
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import { mapState } from "vuex";

  export default {
    name: "DealHistory",
    props: ["deal", "deal_id", "deal_version"],
    computed: {
      ...mapState({
        user: (state) => state.page.user,
      }),
      deduced_position() {
        if (this.deal.versions.length === 0) return 0;
        if (this.deal_version) {
          return this.deal.versions.findIndex(
            (v) => +v.revision.id === +this.deal_version
          );
        }
        for (const [i, v] of this.deal.versions.entries()) {
          if (v.deal.draft_status === null) return i;
        }
        return this.deal.versions.length - 1;
      },
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

        if (draft_status) {
          return draft_status_map[draft_status];
        }

        let st = status_map[status];
        if (draft_status) {
          return `${st} + ${draft_status_map[draft_status]}`;
        }
        return st;
      },
    },
  };
</script>
