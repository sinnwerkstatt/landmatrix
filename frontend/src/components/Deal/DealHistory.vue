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
            <span v-if="(!deal_version && !i) || +deal_version === +version.revision.id"
              >Current</span
            >
            <router-link
              v-else
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
  import { derive_status } from "/utils";
  import { mapState } from "vuex";

  export default {
    name: "DealHistory",
    props: ["deal", "deal_id", "deal_version"],
    methods: {
      derive_status,
    },
    computed: {
      ...mapState({
        user: (state) => state.page.user,
      }),
    },
  };
</script>
