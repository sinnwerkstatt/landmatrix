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
            v-for="opt in filterChoices"
            :key="opt.id"
            :class="{ active: opt.id === selectedTab }"
            class="sidebar-option"
          >
            <div v-if="opt.space" />
            <a
              v-else
              class="whitespace-nowrap"
              :class="[!showDeals && 'text-teal']"
              @click="switchTab(opt.id)"
            >
              {{ $t(opt.name) }}
              <span v-if="opt.count">({{ opt.count }})</span>
            </a>
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
                :options="country_options"
                label="name"
                select-label=""
                placeholder="Country"
              />
              <span @click="setSort('country')">
                {{
                  showDeals
                    ? $t("Target country")
                    : $t("Country of registration/origin")
                }}
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
                :max-date="new Date()"
                mode="date"
                is-range
                :first-day-of-week="2"
                :masks="{ input: 'YYYY-MM-DD' }"
              >
                <template #default="{ inputValue, inputEvents, isDragging }">
                  <div class="flex flex-col sm:flex-row justify-start items-center">
                    <div class="relative flex-grow">
                      <CalendarIcon
                        cls="text-gray-600 w-4 h-full mx-2 absolute pointer-events-none"
                      />
                      <input
                        class="flex-grow !pl-6 pr-2 py-1 bg-gray-100 border rounded w-full"
                        :class="isDragging ? 'text-gray-600' : 'text-gray-900'"
                        :value="inputValue.start"
                        v-on="inputEvents.start"
                      />
                    </div>
                    <div class="relative flex-grow">
                      <CalendarIcon
                        cls="text-gray-600 w-4 h-full mx-2 absolute pointer-events-none"
                      />
                      <input
                        class="flex-grow !pl-6 pr-2 py-1 bg-gray-100 border rounded w-full"
                        :class="isDragging ? 'text-gray-600' : 'text-gray-900'"
                        :value="inputValue.end"
                        v-on="inputEvents.end"
                      />
                    </div>
                  </div>
                </template>
              </DatePicker>

              <br />
              <multiselect
                v-if="user_is_staff"
                v-model="created_by"
                :allow-empty="true"
                :close-on-select="true"
                :multiple="false"
                :options="users"
                label="username"
                select-label=""
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
                :max-date="new Date()"
                mode="date"
                is-range
                :first-day-of-week="2"
                :masks="{ input: 'YYYY-MM-DD' }"
              >
                <template #default="{ inputValue, inputEvents, isDragging }">
                  <div class="flex flex-col sm:flex-row justify-start items-center">
                    <div class="relative flex-grow">
                      <CalendarIcon
                        cls="text-gray-600 w-4 h-full mx-2 absolute pointer-events-none"
                      />
                      <input
                        class="flex-grow !pl-6 pr-2 py-1 bg-gray-100 border rounded w-full"
                        :class="isDragging ? 'text-gray-600' : 'text-gray-900'"
                        :value="inputValue.start"
                        v-on="inputEvents.start"
                      />
                    </div>
                    <div class="relative flex-grow">
                      <CalendarIcon
                        cls="text-gray-600 w-4 h-full mx-2 absolute pointer-events-none"
                      />
                      <input
                        class="flex-grow !pl-6 pr-2 py-1 bg-gray-100 border rounded w-full"
                        :class="isDragging ? 'text-gray-600' : 'text-gray-900'"
                        :value="inputValue.end"
                        v-on="inputEvents.end"
                      />
                    </div>
                  </div>
                </template>
              </DatePicker>
              <br />
              <multiselect
                v-if="user_is_staff"
                v-model="modified_by"
                :allow-empty="true"
                :close-on-select="true"
                :multiple="false"
                :options="users"
                label="username"
                select-label=""
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
                :max-date="new Date()"
                mode="date"
                is-range
                :first-day-of-week="2"
                :masks="{ input: 'YYYY-MM-DD' }"
              >
                <template #default="{ inputValue, inputEvents, isDragging }">
                  <div class="flex flex-col sm:flex-row justify-start items-center">
                    <div class="relative flex-grow">
                      <CalendarIcon
                        cls="text-gray-600 w-4 h-full mx-2 absolute pointer-events-none"
                      />
                      <input
                        class="flex-grow !pl-6 pr-2 py-1 bg-gray-100 border rounded w-full"
                        :class="isDragging ? 'text-gray-600' : 'text-gray-900'"
                        :value="inputValue.start"
                        v-on="inputEvents.start"
                      />
                    </div>
                    <div class="relative flex-grow">
                      <CalendarIcon
                        cls="text-gray-600 w-4 h-full mx-2 absolute pointer-events-none"
                      />
                      <input
                        class="flex-grow !pl-6 pr-2 py-1 bg-gray-100 border rounded w-full"
                        :class="isDragging ? 'text-gray-600' : 'text-gray-900'"
                        :value="inputValue.end"
                        v-on="inputEvents.end"
                      />
                    </div>
                  </div>
                </template>
              </DatePicker>
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
                :options="status_options"
                :placeholder="$t('Status')"
                label="name"
                track-by="id"
                select-label=""
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
                :object-version="obj.current_draft && obj.current_draft.id"
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
  import CalendarIcon from "$components/icons/Calendar.vue";
  import { sortAnything } from "$utils";
  import { combined_status_fn } from "$utils/choices";
  // @ts-ignore
  import DatePicker from "v-calendar/lib/components/date-picker.umd";

  import type { User } from "$types/user";
  import type { Investor } from "$types/investor";
  import type { Deal } from "$types/deal";
  import type { GQLFilter } from "$types/filters";
  import type { Country, Region } from "$types/wagtail";

  dayjs.extend(isSameOrBefore);
  dayjs.extend(isSameOrAfter);

  type FilterChoice = {
    name?: string;
    id?: string;
    staff?: boolean;
    space?: boolean;
    filters?: GQLFilter[];
    count?: number;
    onlyForDeals?: boolean;
  };

  export default Vue.extend({
    name: "Management",
    components: { CalendarIcon, LoadingPulse, DisplayField, DatePicker },
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
              current_draft {
                id
              }
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
          return { filters: this.currentFilters };
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
                country {
                  fk_region {
                    id
                  }
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
        fetchPolicy: "no-cache",
        debounce: 300,
      },
    },
    computed: {
      user(): User {
        return this.$store.state.user;
      },
      user_is_staff(): boolean {
        return this.$store.getters.userInGroup(["Administrators", "Editors"]);
      },
      region(): Region | null {
        const regions = this.user.userregionalinfo?.region;
        if (regions?.length > 0) return regions[0];
        return null;
      },
      country_options(): Country[] {
        const seen_ids = [] as number[];
        const countries = [] as Country[];
        this.objects.forEach((o: Deal | Investor) => {
          if (!o.country) return;
          if (seen_ids.includes(o.country.id)) return;
          seen_ids.push(o.country.id);
          countries.push(o.country);
        });
        return countries.sort((a, b) => a.name.localeCompare(b.name));
      },
      status_options(): { id: string; name: string }[] {
        const seen_ids = [] as string[];
        const status_options = [] as { id: string; name: string }[];
        this.objects.forEach((o: Deal | Investor) => {
          const name = combined_status_fn(o.status, o.draft_status, true);
          const id = combined_status_fn(o.status, o.draft_status, false);
          if (seen_ids.includes(id)) return;
          console.log(o.status, o.draft_status);
          status_options.push({ id, name });
          seen_ids.push(id);
        });
        return status_options;
      },
      objects(): Array<Deal | Investor> {
        let objects = this.showDeals ? this.deals : this.investors;
        if (!objects || objects.length === 0) return [];

        objects = sortAnything(
          objects.map((o) => ({ ...o, combined_status: [o.status, o.draft_status] })),
          this.sortField,
          this.sortAscending
        );
        if (this.region)
          if (this.showDeals)
            objects = objects.filter(
              (o) => o.country?.fk_region?.id === this.region.id
            );
          else
            objects = objects.filter((o) => {
              const deal_regions = o.deals.map((d) => d.country?.fk_region?.id);
              console.log(deal_regions, this.region.id);
              return deal_regions.includes(this.region.id);
            });

        if (this.selected_country)
          objects = objects.filter((o) => o.country?.id === this.selected_country.id);

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
            case "DELETED":
              objects = objects.filter((o) => o.status === 4);
              break;
            case "DRAFT":
              objects = objects.filter((o) => o.draft_status === 1);
              break;
            case "REVIEW":
              objects = objects.filter((o) => o.draft_status === 2);
              break;
            case "ACTIVATION":
              objects = objects.filter((o) => o.draft_status === 3);
              break;
            case "REJECTED":
              objects = objects.filter((o) => o.draft_status === 4);
              break;
            case "TO_DELETE":
              objects = objects.filter((o) => o.draft_status === 5);
              break;
            case "LIVE":
              objects = objects.filter(
                (o) => [2, 3].includes(o.status) && o.draft_status === null
              );
              break;
          }
          console.log(this.selected_combined_status);
        }

        return objects;
      },
      filterChoices(): FilterChoice[] {
        const all_opts = [
          {
            name: "Todo: Clarification",
            id: "todo_clarification",
            filters: [
              { field: "workflowinfos.draft_status_before", value: null },
              { field: "workflowinfos.draft_status_after", value: null },
              { field: "workflowinfos.to_user_id", value: this.user.id },
            ],
          },
          {
            name: "Todo: Improve",
            id: "todo_improve",
            filters: [
              { field: "draft_status", value: 1 },
              { field: "workflowinfos.draft_status_before", value: 2 },
              { field: "workflowinfos.draft_status_after", value: 1 },
              { field: "workflowinfos.to_user_id", value: this.user.id },
            ],
          },
          {
            name: "Todo: Review",
            id: "todo_review",
            staff: true,
            filters: [{ field: "draft_status", value: 2 }],
          },
          {
            name: "Todo: Activation",
            id: "todo_activation",
            staff: true,
            filters: [{ field: "draft_status", value: 3 }],
          },
          { space: true, staff: true },
          {
            name: "Requested improvement",
            id: "requested_improvement",
            staff: true,
            filters: [
              { field: "workflowinfos.draft_status_before", value: 2 },
              { field: "workflowinfos.draft_status_after", value: 1 },
              { field: "workflowinfos.from_user_id", value: this.user.id },
            ],
          },
          {
            name: "Requested feedback",
            id: "requested_feedback",
            filters: [
              { field: "workflowinfos.draft_status_before", value: null },
              { field: "workflowinfos.draft_status_after", value: null },
              { field: "workflowinfos.from_user_id", value: this.user.id },
            ],
          },
          { space: true },
          {
            name: "My drafts",
            id: "my_drafts",
            filters: [
              { field: "draft_status", value: 1 },
              {
                field: "current_draft.created_by_id",
                value: this.user.id,
              },
            ],
          },
          {
            name: "Created by me",
            id: "created_by_me",
            filters: [{ field: "created_by_id", value: this.user.id }],
          },
          {
            name: "Reviewed by me",
            id: "reviewed_by_me",
            staff: true,
            filters: [
              { field: "workflowinfos.draft_status_before", value: 2 },
              { field: "workflowinfos.draft_status_after", value: 3 },
              { field: "workflowinfos.from_user_id", value: this.user.id },
            ],
          },
          {
            name: "Activated by me",
            id: "activated_by_me",
            staff: true,
            filters: [
              { field: "workflowinfos.draft_status_before", value: 3 },
              { field: "workflowinfos.from_user_id", value: this.user.id },
            ],
          },
          { space: true, staff: true },
          {
            name: "All drafts",
            id: "all_drafts",
            staff: true,
            filters: [{ field: "current_draft", exclusion: true, value: null }],
          },
          {
            name: "All deleted",
            id: "all_deleted",
            staff: true,
            filters: [{ field: "status", value: 4 }],
          },
          // {
          //   name: "All not public",
          //   id: "all_not_public",
          //   staff: true,
          //   filters: [{ field: "is_public", value: false }],
          //   onlyForDeals: true,
          // },
        ];
        return all_opts.filter((o) => this.user_is_staff || o.staff !== true);
      },
      currentFilters(): GQLFilter[] {
        const sidebarOption = this.filterChoices.find(
          (s: FilterChoice) => s.id === this.selectedTab
        );
        return sidebarOption.filters;
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
      showDeals() {
        console.log("changing 'showDeals'");
        this.filterChoices.forEach((sopt: FilterChoice) => this.calc_count(sopt));
      },
    },
    created() {
      this.filterChoices.forEach((sopt: FilterChoice) => this.calc_count(sopt));
    },
    methods: {
      async calc_count(query: FilterChoice): Promise<void> {
        if (!query.filters || (query.onlyForDeals && !this.showDeals)) return;
        let xx;
        if (this.showDeals) {
          xx = await this.$apollo.query({
            query: gql`
              query deals($filters: [Filter]) {
                deals(limit: 0, filters: $filters, subset: UNFILTERED) {
                  id
                }
              }
            `,
            variables: { filters: query.filters },
          });
          query.count = xx.data.deals.length;
        } else {
          xx = await this.$apollo.query({
            query: gql`
              query investors($filters: [Filter]) {
                investors(limit: 0, filters: $filters, subset: UNFILTERED) {
                  id
                }
              }
            `,
            variables: { filters: query.filters },
          });
          query.count = xx.data.investors.length;
        }
      },
      updatePagedRows(): void {
        const PAGESIZE = 20;
        let startIndex = (this.page - 1) * PAGESIZE;
        let endIndex = Math.min(this.page * PAGESIZE, this.objects.length);
        this.disableLoader = this.page * PAGESIZE > this.objects.length;
        this.page++;
        this.rows = [...this.rows, ...this.objects.slice(startIndex, endIndex)];
      },
      setSort(field: string): void {
        if (this.sortField === field) this.sortAscending = !this.sortAscending;
        this.sortField = field;
      },
      switchTab(tab: string): void {
        this.selectedTab = tab;
        localStorage.management_selectedTab = tab;
        this.selected_country = null;
        this.selected_from_size = null;
        this.selected_to_size = null;
        this.created_daterang = null;
        this.created_by = null;
        this.modified_daterange = null;
        this.modified_b = null;
        this.fully_updated_daterang = null;
        this.selected_combined_status = null;
      },
    },
  });
</script>

<style lang="scss" scoped>
  .management {
    @apply flex w-full border-lm-dark border h-[calc(100vh-60px-31px)];
  }

  .sidebar {
    @apply h-full p-2 flex-auto;

    .sidebar-options {
      @apply border-r border-orange h-full;
      &.clr-investor {
        @apply border-teal;
      }
    }
    .sidebar-header {
      @apply border-b border-gray-200 p-1;

      div {
        @apply mr-3 px-1 pb-1 inline font-bold;

        &.active {
          @apply border-b border-solid border-black;
        }
        @apply hover:text-gray-600 hover:border-gray-200;
      }
    }
  }

  .management-main {
    @apply flex-auto overflow-auto max-h-full w-full;
  }

  .bigtable {
    thead {
      @apply border-b-4 border-orange;

      tr th {
        @apply whitespace-nowrap;
      }

      th {
        color: white;

        span.selected {
          @apply text-orange;
          //color: var(--color-lm-orange);

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
        @apply border-b-4 border-teal;
      }
    }

    td.field-workflowinfos {
      @apply max-w-[100px];
    }
  }
</style>
