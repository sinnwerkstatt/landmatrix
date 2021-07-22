<template>
  <div class="management">
    <LoadingPulse v-if="$apollo.loading" />
    <div class="sidebar">
      <div class="sidebar-header">
        <div :class="{ active: showDeals }" @click="showDeals = true">Deals</div>
        <div :class="{ active: !showDeals }" @click="showDeals = false">Investors</div>
      </div>
      <div class="sidebar-options">
        <div
          v-for="opt in sidebarOptions"
          class="sidebar-option"
          :class="{ active: opt.id === selectedTab }"
        >
          <div @click="selectedTab = opt.id">{{ opt.name }}</div>
        </div>
      </div>
    </div>
    <div class="management-main">
      <table class="bigtable">
        <thead>
          <tr>
            <th>ID</th>
            <th>
              <input placeholder="Country" /><br />
              <input placeholder="Region" /><br />
              Target country (region)
            </th>

            <th>
              <input placeholder="From size" /><br />
              <input placeholder="To size" /><br />
              Deal size
            </th>
            <th>Created</th>
            <th>Last modified</th>
            <th>Comments / History</th>
            <th>
              <input placeholder="Status" /><br />
              Status
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="deal in deals" :key="deal.id">
            <td v-for="fieldName in fields" :key="`${deal.id}-${fieldName}`">
              <DisplayField
                :fieldname="fieldName"
                :value="deal[fieldName]"
                :model="targetModel"
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
        selectedTab: "my_drafts",
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
      },
    },
    computed: {
      sidebarOptions() {
        return [
          { name: "Todo: Clarification" },
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
        switch (this.selectedTab) {
          case "todo_improve":
            return [
              { field: "draft_status", operation: "EQ", value: "1" },
              // this does not work
              {
                field: "current_draft.workflowinfos.draft_status_before",
                operation: "EQ",
                value: "2",
              },
              {
                field: "current_draft.workflowinfos.draft_status_before",
                operation: "EQ",
                value: "1",
              },
            ];
          case "todo_review":
            return [{ field: "draft_status", operation: "EQ", value: "2" }];
          case "todo_activation":
            return [{ field: "draft_status", operation: "EQ", value: "3" }];
          case "my_drafts":
            return [
              {
                field: "current_draft.revision.user_id",
                operation: "EQ",
                value: this.$store.state.page.user.id.toString(),
              },
            ];
          case "created_by_me":
            return [
              {
                field: "created_by_id",
                operation: "EQ",
                value: this.$store.state.page.user.id.toString(),
              },
            ];
          case "reviewed_by_me":
            return [
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
            ];
          case "activated_by_me":
            return [
              {
                field: "workflowinfos.draft_status_before",
                value: "3",
              },
              {
                field: "workflowinfos.from_user_id",
                value: this.$store.state.page.user.id.toString(),
              },
            ];
          case "all_drafts":
            return [
              {
                field: "draft_status",
                operation: "IN",
                value: ["1", "2", "3"],
              },
            ];
          case "all_deleted":
            return [
              {
                field: "status",
                operation: "EQ",
                value: "4",
              },
            ];
          case "all_not_public":
            return [{ field: "is_public", operation: "EQ", value: "False" }];
        }
        return [{ field: "draft_status", operation: "EQ", value: "-1" }];
      },
      fields() {
        return [
          "id",
          "country",
          "deal_size",
          "created_at",
          "modified_at",
          "workflowinfos",
          "status",
        ];
      },
      targetModel() {
        return "deal";
      },
    },
    methods: {},
  };
</script>
<style scoped lang="scss">
  .management {
    display: grid;
    grid-template-columns: minmax(200px, 1fr) 4fr;
    grid-template-rows: 1fr;
    width: 100%;
    height: calc(100vh - 60px - 35px - 39px);
  }
  .sidebar {
    padding: 0.2rem;
    background: blanchedalmond;
    overflow-y: auto;
    max-height: 100%;
    .sidebar-header div {
      padding: 0.2rem;
      display: inline;
      font-weight: bold;
      &.active {
        border-bottom: 1px solid;
      }
    }
    .active {
      font-weight: bold;
    }
  }
  .management-main {
    overflow-y: auto;
    max-height: 100%;
  }
</style>
