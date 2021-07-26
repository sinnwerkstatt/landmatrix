<template>
  <div class="management">
    <LoadingPulse v-if="$apollo.loading" />
    <div class="sidebar">
      <div class="sidebar-header">
        <div :class="{ active: showDeals }" @click="showDeals = true">Deals</div>
        <div :class="{ active: !showDeals }" @click="showDeals = false">Investors</div>
      </div>
      <div class="sidebar-options">
        <ul class="lm-nav" :class="{ 'clr-investor': !showDeals }">
          <li
            v-for="opt in sidebarOptions"
            :key="opt.id"
            class="sidebar-option"
            :class="{ active: opt.id === selectedTab }"
          >
            <div @click="selectedTab = opt.id">{{ opt.name }}</div>
          </li>
        </ul>
      </div>
    </div>
    <div class="management-main">
      <table class="bigtable" :class="{ 'clr-investor': !showDeals }">
        <thead>
          <tr>
            <th>{{ $t("ID") }}</th>
            <th v-if="!showDeals">{{ $t("Name") }}</th>
            <th>
              <multiselect
                v-model="selected_country"
                :options="$store.state.page.countries"
                label="name"
                placeholder="Country"
              />
              <input placeholder="Region" /><br />

              {{ $t("Target country (region)") }}
            </th>

            <th v-if="showDeals">
              <input v-model="selected_from_size" placeholder="From size" /><br />
              <input v-model="selected_to_size" placeholder="To size" /><br />
              {{ $t("Deal size") }}
            </th>
            <th>
              <input placeholder="Daterange" /><br />
              <input placeholder="User" /><br />
              {{ $t("Created") }}
            </th>
            <th>
              <input placeholder="Daterange" /><br />
              <input placeholder="User" /><br />
              {{ $t("Last modified") }}
            </th>
            <th v-if="showDeals">
              <input placeholder="Daterange" /><br />
              <input placeholder="User" /><br />
              {{ $t("Fully updated") }}
            </th>
            <th>{{ $t("Comments / History") }}</th>
            <th>
              <input placeholder="Status" /><br />
              {{ $t("Status") }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="deal in showDeals ? deals : investors" :key="deal.id">
            <td
              v-for="fieldName in fields"
              :key="`${deal.id}-${fieldName}`"
              :class="`field-${fieldName}`"
            >
              <DisplayField
                :fieldname="fieldName"
                :value="deal[fieldName]"
                :model="showDeals ? 'deal' : 'investor'"
                :show-label="false"
                :value-classes="[]"
                :wrapper-classes="[]"
              />
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
  import LoadingPulse from "$components/Data/LoadingPulse";
  import DisplayField from "$components/Fields/DisplayField";
  import gql from "graphql-tag";

  export default {
    name: "Manager",
    components: { LoadingPulse, DisplayField },
    data() {
      return {
        showDeals: true,
        deals: [],
        investors: [],
        selectedTab: "my_drafts",
        selected_country: null,
        selected_from_size: null,
        selected_to_size: null,
      };
    },
    apollo: {
      deals: {
        query: gql`
          query deals($filters: [Filter]) {
            deals(limit: 0, filters: $filters, subset: UNFILTERED) {
              id
              deal_size
              created_at
              created_by {
                id
                username
              }
              modified_at
              modified_by {
                id
                username
              }

              fully_updated_at
              status
              draft_status
              country {
                name
                fk_region {
                  name
                }
              }
              workflowinfos {
                id
                comment
                timestamp
                from_user {
                  id
                  username
                }
                to_user {
                  id
                  username
                }
              }
            }
          }
        `,
        variables() {
          return {
            filters: this.currentFilters,
          };
        },
        skip() {
          return !this.showDeals;
        },
        debounce: 300,
      },
      investors: {
        query: gql`
          query investors($filters: [Filter]) {
            investors(limit: 0, filters: $filters, subset: UNFILTERED) {
              id
              name
              created_at
              modified_at

              status
              draft_status
              country {
                name
                fk_region {
                  name
                }
              }
              workflowinfos {
                id
                comment
                timestamp
                from_user {
                  username
                }
                to_user {
                  username
                }
              }
            }
          }
        `,
        variables() {
          return {
            filters: this.currentFilters,
          };
        },
        skip() {
          return this.showDeals;
        },
        debounce: 300,
      },
    },
    computed: {
      sidebarOptions() {
        return [
          { name: "Todo: Clarification", id: "todo_clarification" },
          { name: "Todo: Improve", id: "todo_improve" },
          { name: "Todo: Review", id: "todo_review" },
          { name: "Todo: Activation", id: "todo_activation" },
          { name: "My drafts", id: "my_drafts" },
          { name: "Created by me", id: "created_by_me" },
          { name: "Reviewed by me", id: "reviewed_by_me" },
          { name: "Activated by me", id: "activated_by_me" },
          { name: "All drafts", id: "all_drafts" },
          { name: "All deleted", id: "all_deleted" },
          { name: "All not public", id: "all_not_public" },
        ];
      },
      currentFilters() {
        let retfilters = [];
        if (this.selected_country)
          retfilters.push({
            field: "country_id",
            value: this.selected_country.id.toString(),
          });

        if (this.showDeals && this.selected_from_size) {
          retfilters.push({
            field: "deal_size",
            operation: "GE",
            value: this.selected_from_size.toString(),
          });
        }
        if (this.showDeals && this.selected_to_size) {
          retfilters.push({
            field: "deal_size",
            operation: "LE",
            value: this.selected_to_size.toString(),
          });
        }

        switch (this.selectedTab) {
          case "todo_clarification":
            // TODO
            retfilters.push({ field: "status", value: "7" });
            break;
          case "todo_improve":
            console.log("imrpv");
            retfilters.push(
              ...[
                // { field: "draft_status", value: "1" },
                // TODO this does not work
                {
                  field: "current_draft.workflowinfos.draft_status_before",
                  value: "2",
                },
                {
                  field: "current_draft.workflowinfos.draft_status_before",
                  value: "1",
                },
              ]
            );
            break;
          case "todo_review":
            retfilters.push({ field: "draft_status", operation: "EQ", value: "2" });
            break;
          case "todo_activation":
            retfilters.push({ field: "draft_status", operation: "EQ", value: "3" });
            break;
          case "my_drafts":
            retfilters.push({
              field: "current_draft.revision.user_id",
              operation: "EQ",
              value: this.$store.state.page.user.id.toString(),
            });
            break;
          case "created_by_me":
            retfilters.push({
              field: "created_by_id",
              operation: "EQ",
              value: this.$store.state.page.user.id.toString(),
            });
            break;
          case "reviewed_by_me":
            retfilters.push(
              ...[
                {
                  field: "workflowinfos.draft_status_before",
                  value: "2",
                },
                {
                  field: "workflowinfos.draft_status_after",
                  value: "3",
                },
                {
                  field: "workflowinfos.from_user_id",
                  value: this.$store.state.page.user.id.toString(),
                },
              ]
            );
            break;
          case "activated_by_me":
            retfilters.push(
              ...[
                {
                  field: "workflowinfos.draft_status_before",
                  value: "3",
                },
                {
                  field: "workflowinfos.from_user_id",
                  value: this.$store.state.page.user.id.toString(),
                },
              ]
            );
            break;
          case "all_drafts":
            retfilters.push({
              field: "draft_status",
              operation: "IN",
              value: ["1", "2", "3"],
            });
            break;
          case "all_deleted":
            retfilters.push({ field: "status", operation: "EQ", value: "4" });
            break;
          case "all_not_public":
            retfilters.push({ field: "is_public", operation: "EQ", value: "False" });
            break;
        }
        return retfilters;
      },
      fields() {
        return this.showDeals
          ? [
              "id",
              "country",
              "deal_size",
              "created_at",
              "modified_at",
              "fully_updated_at",
              "workflowinfos",
              "status",
            ]
          : [
              "id",
              "name",
              "country",
              "created_at",
              "modified_at",
              "workflowinfos",
              "status",
            ];
      },
    },
    methods: {},
  };
</script>
<style scoped lang="scss">
  .management {
    display: flex;
    width: 100%;
    height: calc(100vh - 60px - 35px - 39px);
    padding-left: 1em;
    padding-right: 1em;
  }
  .sidebar {
    width: 11rem;
    min-width: 11rem;
    padding: 0.2rem;
    overflow-y: auto;
    max-height: 100%;
    .sidebar-header {
      border-bottom: 1px solid #dee2e6;
      padding: 0.2rem;

      div {
        //margin-left: 0.4rem;
        //padding-left: 0.4rem;
        margin-right: 0.6rem;
        padding-bottom: 0.2rem;
        display: inline;
        font-weight: bold;

        &.active {
          border-bottom: 1px solid;
        }

        &:hover {
          border-color: #e9ecef #e9ecef #dee2e6;
        }
      }
    }
    .active {
      font-weight: bold;
    }
  }
  .management-main {
    overflow-y: auto;
    max-height: 100%;
    overflow-x: auto;
    //width: min(99%, 90em);
  }

  .bigtable {
    thead {
      border-bottom: 3px solid var(--color-lm-orange);
      //border-collapse: separate;
      tr th {
        white-space: nowrap;
      }
    }
    &.clr-investor {
      thead {
        border-bottom: 3px solid var(--color-lm-investor);
      }
    }
    td.field-workflowinfos {
      max-width: 100px;
    }
  }
</style>
