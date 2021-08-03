<template>
  <div class="management">
    <LoadingPulse v-if="$apollo.loading" />
    <div class="sidebar">
      <div class="sidebar-header">
        <div :class="{ active: showDeals }" @click="showDeals = true">Deals</div>
        <div :class="{ active: !showDeals }" @click="showDeals = false">Investors</div>
      </div>
      <div class="sidebar-options">
        <ul :class="{ 'clr-investor': !showDeals }" class="lm-nav">
          <li
            v-for="opt in sidebarOptions"
            :key="opt.id"
            :class="{ active: opt.id === selectedTab }"
            class="sidebar-option"
          >
            <div v-if="opt.space" />
            <a v-else @click="selectedTab = opt.id">{{ opt.name }}</a>
          </li>
        </ul>
      </div>
    </div>
    <div class="management-main">
      <table :class="{ 'clr-investor': !showDeals }" class="bigtable">
        <thead>
          <tr>
            <th :class="{ selected: sortField === 'id', asc: sortAscending }">
              <span @click="setSort('id')">
                {{ $t("ID") }}
              </span>
            </th>
            <th
              v-if="!showDeals"
              :class="{ selected: sortField === 'name', asc: sortAscending }"
            >
              <span @click="setSort('name')">
                {{ $t("Name") }}
              </span>
            </th>
            <th :class="{ selected: sortField === 'country', asc: sortAscending }">
              <multiselect
                v-model="selected_country"
                :options="$store.state.page.countries"
                label="name"
                placeholder="Country"
                @input="selected_region = null"
              />
              <multiselect
                v-model="selected_region"
                :options="$store.state.page.regions"
                label="name"
                placeholder="Region"
                @input="selected_country = null"
              />
              <span @click="setSort('country')">
                {{ $t("Target country (region)") }}
              </span>
            </th>

            <th
              v-if="showDeals"
              :class="{ selected: sortField === 'deal_size', asc: sortAscending }"
            >
              <input v-model="selected_from_size" placeholder="From size" /><br />
              <input v-model="selected_to_size" placeholder="To size" /><br />
              <span @click="setSort('deal_size')">{{ $t("Deal size") }}</span>
            </th>
            <th :class="{ selected: sortField === 'created_at', asc: sortAscending }">
              <DatePicker
                v-model="created_daterange"
                :input-props="{ style: 'width: 100%' }"
                :max-date="new Date()"
                mode="range"
              />
              <br />
              <!--              <multiselect-->
              <!--                v-if="user_is_staff"-->
              <!--                v-model="created_by"-->
              <!--                :options="users"-->
              <!--                :multiple="false"-->
              <!--                :close-on-select="true"-->
              <!--                :allow-empty="true"-->
              <!--                placeholder="User"-->
              <!--                track-by="id"-->
              <!--                label="username"-->
              <!--              />-->
              <span @click="setSort('created_at')">{{ $t("Created") }}</span>
            </th>
            <th :class="{ selected: sortField === 'modified_at', asc: sortAscending }">
              <DatePicker
                v-model="modified_daterange"
                :input-props="{ style: 'width: 100%' }"
                :max-date="new Date()"
                mode="range"
              />
              <br />
              <!--              <multiselect-->
              <!--                v-if="user_is_staff"-->
              <!--                v-model="modified_by"-->
              <!--                :options="users"-->
              <!--                :multiple="false"-->
              <!--                :close-on-select="true"-->
              <!--                :allow-empty="true"-->
              <!--                placeholder="User"-->
              <!--                track-by="id"-->
              <!--                label="username"-->
              <!--              />-->
              <span @click="setSort('modified_at')">{{ $t("Last modified") }}</span>
            </th>
            <th
              v-if="showDeals"
              :class="{
                selected: sortField === 'fully_updated_at',
                asc: sortAscending,
              }"
            >
              <DatePicker
                v-model="fully_updated_daterange"
                :input-props="{ style: 'width: 100%' }"
                :max-date="new Date()"
                mode="range"
              />
              <br />
              <span @click="setSort('fully_updated_at')">
                {{ $t("Fully updated") }}
              </span>
            </th>
            <th class="comments_header">{{ $t("Comments / History") }}</th>
            <th
              :class="{
                selected: sortField === 'status',
                asc: sortAscending,
              }"
            >
              <input placeholder="Status" /><br />
              <span @click="setSort('status')">{{ $t("Status") }}</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="obj in objects" :key="obj.id">
            <td
              v-for="fieldName in fields"
              :key="`${obj.id}-${fieldName}`"
              :class="`field-${fieldName}`"
            >
              <DisplayField
                :fieldname="fieldName"
                :model="showDeals ? 'deal' : 'investor'"
                :show-label="false"
                :target-blank="true"
                :value="obj[fieldName]"
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
  import { sortAnything } from "$utils";
  import dayjs from "dayjs";
  import gql from "graphql-tag";
  import DatePicker from "v-calendar/lib/components/date-picker.umd";

  // // Register components in your 'main.js'
  // Vue.component('calendar', Calendar)
  // Vue.component('date-picker', DatePicker)

  export default {
    name: "Manager",
    components: { LoadingPulse, DisplayField, DatePicker },
    metaInfo() {
      return { title: this.$t("Management") };
    },
    data() {
      return {
        showDeals: true,
        users: [],
        deals: [],
        investors: [],
        sortField: "id",
        sortAscending: false,
        selectedTab: "my_drafts",
        selected_region: null,
        selected_country: null,
        selected_from_size: null,
        selected_to_size: null,
        created_daterange: null,
        created_by: null,
        modified_daterange: null,
        modified_by: null,
        fully_updated_daterange: null,
      };
    },
    apollo: {
      users: gql`
        {
          users {
            id
            full_name
            username
          }
        }
      `,

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
                id
                name
                fk_region {
                  id
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
                id
                name
                fk_region {
                  id
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
          return this.showDeals;
        },
        debounce: 300,
      },
    },
    computed: {
      user() {
        return this.$store.state.page.user;
      },
      user_is_staff() {
        return this.$store.getters.userInGroup(["Administrators", "Editors"]);
      },
      objects() {
        return sortAnything(
          this.showDeals ? this.deals : this.investors,
          this.sortField,
          this.sortAscending
        );
      },
      sidebarOptions() {
        const all_opts = [
          { name: "Todo: Clarification", id: "todo_clarification" },
          { name: "Todo: Improve", id: "todo_improve" },
          { name: "Todo: Review", id: "todo_review", staff: true },
          { name: "Todo: Activation", id: "todo_activation", staff: true },
          { name: "New public comment", id: "new_public_comment", staff: true },
          { space: true, staff: true },
          { name: "Requested improvement", id: "requested_improvement", staff: true },
          { name: "Requested feedback", id: "requested_feedback", staff: true },
          { space: true },
          { name: "My drafts", id: "my_drafts" },
          { name: "Created by me", id: "created_by_me" },
          { name: "Reviewed by me", id: "reviewed_by_me", staff: true },
          { name: "Activated by me", id: "activated_by_me", staff: true },
          { space: true, staff: true },
          { name: "All drafts", id: "all_drafts", staff: true },
          { name: "All deleted", id: "all_deleted", staff: true },
          { name: "All not public", id: "all_not_public", staff: true },
        ];
        return all_opts.filter((o) => this.user_is_staff || o.staff !== true);
      },
      currentFilters() {
        /** @type GQLFilter[] */
        let retfilters = [];
        if (this.selected_country)
          retfilters.push({ field: "country_id", value: this.selected_country.id });

        if (this.selected_region)
          retfilters.push({
            field: "country.fk_region_id",
            value: this.selected_region.id,
          });

        if (this.showDeals && this.selected_from_size) {
          retfilters.push({
            field: "deal_size",
            operation: "GE",
            value: this.selected_from_size,
          });
        }
        if (this.showDeals && this.selected_to_size) {
          retfilters.push({
            field: "deal_size",
            operation: "LE",
            value: this.selected_to_size,
          });
        }

        if (this.created_daterange) {
          retfilters.push(
            {
              field: "created_at",
              operation: "GE",
              value: dayjs(this.created_daterange.start).format("YYYY-MM-DD"),
            },
            {
              field: "created_at",
              operation: "LE",
              value: dayjs(this.created_daterange.end).format("YYYY-MM-DD"),
            }
          );
        }
        if (this.created_by)
          retfilters.push({ field: "created_by", value: this.created_by.id });

        if (this.modified_daterange) {
          retfilters.push(
            {
              field: "modified_at",
              operation: "GE",
              value: dayjs(this.modified_daterange.start).format("YYYY-MM-DD"),
            },
            {
              field: "modified_at",
              operation: "LE",
              value: dayjs(this.modified_daterange.end).format("YYYY-MM-DD"),
            }
          );
        }
        if (this.modified_by)
          retfilters.push({ field: "modified_by", value: this.modified_by.id });

        if (this.fully_updated_daterange) {
          retfilters.push(
            {
              field: "fully_updated_at",
              operation: "GE",
              value: dayjs(this.fully_updated_daterange.start).format("YYYY-MM-DD"),
            },
            {
              field: "fully_updated_at",
              operation: "LE",
              value: dayjs(this.fully_updated_daterange.end).format("YYYY-MM-DD"),
            }
          );
        }

        // selected Tab
        switch (this.selectedTab) {
          case "todo_clarification":
            retfilters.push(
              ...[
                // { field: "workflowinfos.processed_by_receiver", value: false },
                { field: "workflowinfos.draft_status_before", value: null },
                { field: "workflowinfos.draft_status_after", value: null },
                { field: "workflowinfos.to_user_id", value: this.user.id },
              ]
            );
            break;
          case "todo_improve":
            retfilters.push(
              ...[
                { field: "draft_status", value: 1 },
                { field: "current_draft.workflowinfos.draft_status_before", value: 2 },
                { field: "current_draft.workflowinfos.draft_status_after", value: 1 },
                {
                  field: "current_draft.workflowinfos.to_user_id",
                  value: this.user.id,
                },
              ]
            );
            break;
          case "todo_review":
            retfilters.push({ field: "draft_status", value: 2 });
            break;
          case "todo_activation":
            retfilters.push({ field: "draft_status", value: 3 });
            break;
          case "new_public_comment":
            // TODO
            retfilters.push({ field: "status", value: "7" });
            break;
          case "requested_improvement":
            retfilters.push(
              ...[
                // { field: "workflowinfos.processed_by_receiver", value: false },
                { field: "workflowinfos.draft_status_before", value: 2 },
                { field: "workflowinfos.draft_status_after", value: 1 },
                { field: "workflowinfos.from_user_id", value: this.user.id },
              ]
            );
            break;
          case "requested_feedback":
            retfilters.push(
              ...[
                // { field: "workflowinfos.processed_by_receiver", value: false },
                { field: "workflowinfos.draft_status_before", value: null },
                { field: "workflowinfos.draft_status_after", value: null },
                { field: "workflowinfos.from_user_id", value: this.user.id },
              ]
            );
            break;
          case "my_drafts":
            retfilters.push({
              field: "current_draft.revision.user_id",
              value: this.user.id,
            });
            break;
          case "created_by_me":
            retfilters.push({ field: "created_by_id", value: this.user.id });
            break;
          case "reviewed_by_me":
            retfilters.push(
              ...[
                { field: "workflowinfos.draft_status_before", value: 2 },
                { field: "workflowinfos.draft_status_after", value: 3 },
                { field: "workflowinfos.from_user_id", value: this.user.id },
              ]
            );
            break;
          case "activated_by_me":
            retfilters.push(
              ...[
                { field: "workflowinfos.draft_status_before", value: 3 },
                { field: "workflowinfos.from_user_id", value: this.user.id },
              ]
            );
            break;
          case "all_drafts":
            retfilters.push({ field: "draft_status", exclusion: true, value: null });
            break;
          case "all_deleted":
            retfilters.push({ field: "status", value: 4 });
            break;
          case "all_not_public":
            retfilters.push({ field: "is_public", value: false });
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
    methods: {
      setSort(field) {
        if (this.sortField === field) this.sortAscending = !this.sortAscending;
        this.sortField = field;
      },
    },
  };
</script>
<style lang="scss" scoped>
  .management {
    display: flex;
    width: 100%;
    height: calc(100vh - 60px - 31px);
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

      .comments_header {
        cursor: default;
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
