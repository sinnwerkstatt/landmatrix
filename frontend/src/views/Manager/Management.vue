<template>
  <div class="management">
    <LoadingPulse v-if="$apollo.loading" />
    <div class="sidebar">
      <div class="sidebar-header">
        <div :class="{ active: showDeals }" @click="showDeals = true">Deals</div>
        <div :class="{ active: !showDeals }" @click="showDeals = false">Investors</div>
      </div>
      <div :class="{ 'clr-investor': !showDeals }" class="sidebar-options">
        <ul :class="{ 'clr-investor': !showDeals }" class="lm-nav">
          <li
            v-for="opt in sidebarOptions"
            :key="opt.id"
            :class="{ active: opt.id === selectedTab }"
            class="sidebar-option"
          >
            <div v-if="opt.space" />
            <a v-else @click="switchTab(opt.id)">{{ opt.name }}</a>
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
            <th>
              <DatePicker
                v-model="created_daterange"
                :input-props="{ style: 'width: 100%' }"
                :max-date="new Date()"
                mode="range"
              />
              <br />
              <multiselect
                v-if="user_is_staff"
                v-model="created_by"
                :allow-empty="true"
                :close-on-select="true"
                :multiple="false"
                :options="users"
                label="username"
                placeholder="User"
                track-by="id"
              />
              <span
                :class="{ selected: sortField === 'created_at', asc: sortAscending }"
                @click="setSort('created_at')"
                >{{ $t("Created at") }}</span
              >
              /
              <span
                :class="{ selected: sortField === 'created_by', asc: sortAscending }"
                @click="setSort('created_by')"
                >{{ $t("Created by") }}</span
              >
            </th>
            <th :class="{ selected: sortField === 'modified_at', asc: sortAscending }">
              <DatePicker
                v-model="modified_daterange"
                :input-props="{ style: 'width: 100%' }"
                :max-date="new Date()"
                mode="range"
              />
              <br />
              <multiselect
                v-if="user_is_staff"
                v-model="modified_by"
                :allow-empty="true"
                :close-on-select="true"
                :multiple="false"
                :options="users"
                label="username"
                placeholder="User"
                track-by="id"
              />
              <span
                :class="{ selected: sortField === 'modified_at', asc: sortAscending }"
                @click="setSort('modified_at')"
                >{{ $t("Last modified at") }}</span
              >
              /
              <span
                :class="{ selected: sortField === 'modified_by', asc: sortAscending }"
                @click="setSort('modified_by')"
                >{{ $t("Last modified by") }}</span
              >
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
              <multiselect
                v-model="selected_combined_status"
                :allow-empty="true"
                :close-on-select="true"
                :multiple="false"
                :options="combined_status_choices"
                :placeholder="$t('Status')"
                label="name"
                track-by="id"
              />
              <span @click="setSort('status')">{{ $t("Status") }}</span>
            </th>
            <th v-if="!showDeals">
              <span>{{ $t("Deals") }}</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="obj in rows" :key="obj.id">
            <td
              v-for="fieldName in fields"
              :key="`${obj.id}-${fieldName}`"
              :class="`field-${fieldName}`"
            >
              <DisplayField
                :fieldname="fieldName"
                :model="showDeals ? 'deal' : 'investor'"
                :object-id="obj.id"
                :show-label="false"
                :target-blank="true"
                :value="obj[fieldName]"
                :value-classes="[]"
                :wrapper-classes="[]"
              />
              <div v-if="['created_at', 'modified_at'].includes(fieldName)">
                <DisplayField
                  :fieldname="fieldName.replace('_at', '_by')"
                  :model="showDeals ? 'deal' : 'investor'"
                  :object-id="obj.id"
                  :show-label="false"
                  :value="obj[fieldName.replace('_at', '_by')]"
                  :value-classes="[]"
                  :wrapper-classes="[]"
                />
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <scroll-loader :loader-disable="disableLoader" :loader-method="updatePagedRows" />
    </div>
  </div>
</template>

<script lang="ts">
  import Vue from "vue";
  import gql from "graphql-tag";
  import dayjs from "dayjs";
  import isSameOrBefore from "dayjs/plugin/isSameOrBefore";
  import isSameOrAfter from "dayjs/plugin/isSameOrAfter";
  import LoadingPulse from "$components/Data/LoadingPulse.vue";
  import DisplayField from "$components/Fields/DisplayField.vue";
  import { sortAnything } from "$utils";
  import { combined_status_options } from "$utils/choices";
  // @ts-ignore
  import DatePicker from "v-calendar/lib/components/date-picker.umd";

  import type { User } from "$types/user";
  import type { Investor } from "$types/investor";
  import type { Deal } from "$types/deal";
  import type { GQLFilter } from "$types/filters";
  import type { Country, Region } from "$types/wagtail";

  dayjs.extend(isSameOrBefore);
  dayjs.extend(isSameOrAfter);

  type SidebarOption = {
    name?: string;
    id?: string;
    staff?: boolean;
    space?: boolean;
  };

  export default Vue.extend({
    name: "Management",
    components: { LoadingPulse, DisplayField, DatePicker },
    metaInfo() {
      return { title: this.$t("Management").toString() };
    },
    data() {
      return {
        showDeals: true,
        users: [] as User[],
        deals: [] as Deal[],
        investors: [] as Investor[],
        // scrollLoader
        rows: [],
        page: 1,
        disableLoader: false,
        // sorting and filtering
        sortField: "id",
        sortAscending: false,
        selectedTab: localStorage.management_selectedTab || "my_drafts",
        selected_region: null as Region | null,
        selected_country: null as Country | null,
        selected_from_size: null as number | null,
        selected_to_size: null as number | null,
        created_daterange: null as Date | null,
        created_by: null as User | null,
        modified_daterange: null as Date | null,
        modified_by: null as User | null,
        fully_updated_daterange: null as Date | null,
        selected_combined_status: null as { id: string; name: string } | null,
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
                draft_status_after
                draft_status_before
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
        fetchPolicy: "no-cache",
        debounce: 300,
      },
      investors: {
        query: gql`
          query investors($filters: [Filter]) {
            investors(limit: 0, filters: $filters, subset: UNFILTERED) {
              id
              name
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
              deals {
                id
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
        fetchPolicy: "no-cache",
        debounce: 300,
      },
    },
    computed: {
      combined_status_choices(): { id: string; name: string }[] {
        return Object.entries(combined_status_options).map(([k, v]) => ({
          id: k,
          name: this.$t(v).toString(),
        }));
      },
      user(): User {
        return this.$store.state.page.user;
      },
      user_is_staff(): boolean {
        return this.$store.getters.userInGroup(["Administrators", "Editors"]);
      },
      objects(): Array<Deal | Investor> {
        let objects = this.showDeals ? this.deals : this.investors;
        if (!objects || objects.length === 0) return [];

        objects = sortAnything(
          objects.map((o) => ({ ...o, combined_status: [o.status, o.draft_status] })),
          this.sortField,
          this.sortAscending
        );

        if (this.selected_country)
          objects = objects.filter((o) => o.country?.id === this.selected_country.id);
        if (this.selected_region)
          objects = objects.filter(
            (o) => o.country?.fk_region?.id === this.selected_region.id
          );
        if (this.showDeals && this.selected_from_size)
          objects = objects.filter((o) => o.deal_size >= this.selected_from_size);
        if (this.showDeals && this.selected_to_size)
          objects = objects.filter((o) => o.deal_size <= this.selected_to_size);
        if (this.created_daterange)
          objects = objects.filter(
            (o) =>
              dayjs(this.created_daterange.start).isSameOrBefore(o.created_at, "day") &&
              dayjs(this.created_daterange.end).isSameOrAfter(o.created_at, "day")
          );
        if (this.created_by)
          objects = objects.filter((o) => o.created_by?.id === this.created_by.id);

        if (this.modified_daterange)
          objects = objects.filter(
            (o) =>
              dayjs(this.modified_daterange.start).isSameOrBefore(
                o.modified_at,
                "day"
              ) &&
              dayjs(this.modified_daterange.end).isSameOrAfter(o.modified_at, "day")
          );
        if (this.modified_by)
          objects = objects.filter((o) => o.modified_by?.id === this.modified_by.id);

        if (this.fully_updated_daterange)
          objects = objects.filter(
            (o) =>
              dayjs(this.fully_updated_daterange.start).isSameOrBefore(
                o.fully_updated_at,
                "day"
              ) &&
              dayjs(this.fully_updated_daterange.end).isSameOrAfter(
                o.fully_updated_at,
                "day"
              )
          );
        if (this.selected_combined_status) {
          switch (this.selected_combined_status.id) {
            case "DRAFT":
              objects = objects.filter((o) => o.status === 1 && o.draft_status === 1);
              break;
            case "REVIEW":
              objects = objects.filter((o) => o.status === 1 && o.draft_status === 2);
              break;
            case "ACTIVATION":
              objects = objects.filter((o) => o.status === 1 && o.draft_status === 3);
              break;
            case "LIVE":
              objects = objects.filter(
                (o) => [2, 3].includes(o.status) && o.draft_status === null
              );
              break;
            case "LIVE_AND_DRAFT":
              objects = objects.filter(
                (o) => [2, 3].includes(o.status) && o.draft_status
              );
              break;
            case "DELETED":
              objects = objects.filter((o) => o.status === 4);
              break;
          }
          console.log(this.selected_combined_status);
        }

        return objects;
      },
      sidebarOptions(): SidebarOption[] {
        const all_opts = [
          { name: "Todo: Clarification", id: "todo_clarification" },
          { name: "Todo: Improve", id: "todo_improve" },
          { name: "Todo: Review", id: "todo_review", staff: true },
          { name: "Todo: Activation", id: "todo_activation", staff: true },
          // { name: "New public comment", id: "new_public_comment", staff: true },
          { space: true, staff: true },
          { name: "Requested improvement", id: "requested_improvement", staff: true },
          { name: "Requested feedback", id: "requested_feedback" },
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
      currentFilters(): GQLFilter[] {
        let retfilters: GQLFilter[] = [];

        // selected Tab
        switch (this.selectedTab) {
          case "todo_clarification":
            retfilters.push(
              // { field: "workflowinfos.processed_by_receiver", value: false },
              { field: "workflowinfos.draft_status_before", value: null },
              { field: "workflowinfos.draft_status_after", value: null },
              { field: "workflowinfos.to_user_id", value: this.user.id }
            );
            break;
          case "todo_improve":
            retfilters.push(
              { field: "draft_status", value: 1 },
              { field: "workflowinfos.draft_status_before", value: 2 },
              { field: "workflowinfos.draft_status_after", value: 1 },
              {
                field: "current_draft.created_by_id",
                value: this.user.id,
              }
            );
            break;
          case "todo_review":
            retfilters.push({ field: "draft_status", value: 2 });
            break;
          case "todo_activation":
            retfilters.push({ field: "draft_status", value: 3 });
            break;
          // case "new_public_comment":
          //   // TODO-3
          //   retfilters.push({ field: "status", value: "7" });
          //   break;
          case "requested_improvement":
            retfilters.push(
              // { field: "workflowinfos.processed_by_receiver", value: false },
              { field: "workflowinfos.draft_status_before", value: 2 },
              { field: "workflowinfos.draft_status_after", value: 1 },
              { field: "workflowinfos.from_user_id", value: this.user.id }
            );
            break;
          case "requested_feedback":
            retfilters.push(
              // { field: "workflowinfos.processed_by_receiver", value: false },
              { field: "workflowinfos.draft_status_before", value: null },
              { field: "workflowinfos.draft_status_after", value: null },
              { field: "workflowinfos.from_user_id", value: this.user.id }
            );
            break;
          case "my_drafts":
            retfilters.push(
              { field: "draft_status", exclusion: true, value: null },
              {
                field: "current_draft.created_by_id",
                value: this.user.id,
              }
            );
            break;
          case "created_by_me":
            retfilters.push({ field: "created_by_id", value: this.user.id });
            break;
          case "reviewed_by_me":
            retfilters.push(
              { field: "workflowinfos.draft_status_before", value: 2 },
              { field: "workflowinfos.draft_status_after", value: 3 },
              { field: "workflowinfos.from_user_id", value: this.user.id }
            );
            break;
          case "activated_by_me":
            retfilters.push(
              { field: "workflowinfos.draft_status_before", value: 3 },
              { field: "workflowinfos.from_user_id", value: this.user.id }
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
      fields(): string[] {
        return this.showDeals
          ? [
              "id",
              "country",
              "deal_size",
              "created_at",
              "modified_at",
              "fully_updated_at",
              "workflowinfos",
              "combined_status",
            ]
          : [
              "id",
              "name",
              "country",
              "created_at",
              "modified_at",
              "workflowinfos",
              "combined_status",
              "deals",
            ];
      },
    },
    watch: {
      objects() {
        this.page = 0;
        this.rows = [];
        this.updatePagedRows();
      },
    },
    methods: {
      updatePagedRows() {
        const PAGESIZE = 20;
        let startIndex = (this.page - 1) * PAGESIZE;
        let endIndex = Math.min(this.page * PAGESIZE, this.objects.length);
        this.disableLoader = this.page * PAGESIZE > this.objects.length;
        this.page++;
        this.rows = [...this.rows, ...this.objects.slice(startIndex, endIndex)];
      },
      setSort(field: string) {
        if (this.sortField === field) this.sortAscending = !this.sortAscending;
        this.sortField = field;
      },
      switchTab(tab: string) {
        this.selectedTab = tab;
        localStorage.management_selectedTab = tab;
      },
    },
  });
</script>

<style lang="scss" scoped>
  .management {
    display: flex;
    width: 100%;
    height: calc(100vh - 60px - 31px);
    //margin-top: 1em;
    border: 1px solid var(--color-lm-dark);

    //padding-left: 1.5em;
    //padding-right: 1em;
  }

  .sidebar {
    width: 12rem;
    min-width: 12rem;
    padding: 0.4rem;
    overflow-y: hidden;
    height: 100%;

    .sidebar-options {
      border-right: 1px solid var(--color-lm-orange);
      height: 100%;
      &.clr-investor {
        border-right: 1px solid var(--color-lm-investor);
      }
    }
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
    width: 100%;
    //width: min(99%, 90em);
  }

  .bigtable {
    thead {
      border-bottom: 3px solid var(--color-lm-orange);
      //border-collapse: separate;
      tr th {
        white-space: nowrap;
      }

      th {
        color: white;

        span.selected {
          color: var(--color-lm-orange);

          &.asc:after {
            margin-left: 0.3rem;
            font-weight: 600;
            content: "\f077";
            //noinspection CssNoGenericFontName
            font-family: "Font Awesome 5 Free";
          }

          &:not(.asc):after {
            margin-left: 0.3rem;
            font-weight: 600;
            content: "\f078";
            //noinspection CssNoGenericFontName
            font-family: "Font Awesome 5 Free";
          }
        }
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
