<template>
  <div class="deal-table">
    <b-pagination
      v-model="currentPage"
      :total-rows="deals.length"
      :per-page="pageSize"
      align="center"
      limit="12"
    ></b-pagination>
    <table id="summary" class="table table-striped">
      <thead>
        <tr>
          <th
            @click="setSort('id')"
            :class="{ selected: sortField === 'id', asc: sortAscending }"
          >
            #
          </th>
          <th
            v-for="field in fields"
            :key="field"
            @click="setSort(field)"
            :class="{ selected: sortField === field, asc: sortAscending }"
          >
            {{ fieldNameMap[field] || field }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="deal in dt_deals" :key="deal.id">
          <td>
            <router-link
              :to="{ name: 'deal_detail', params: { deal_id: deal.id } }"
              v-slot="{ href }"
            >
              <a :href="href">{{ deal.id }}</a>
            </router-link>
          </td>
          <td v-for="field in fields" :key="field" v-html="displayField(deal, field)"></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import {sortAnything} from "../../utils";

  const slugify = require("slugify");

  const STATUS_MAP = {
    1: "Draft",
    2: "Active",
    3: "Active",
    4: "Deleted",
    5: "Rejected",
    6: "To Delete",
  };

  const DRAFT_STATUS_MAP = {
    1: "Draft",
    2: "Review",
    3: "Activation",
  };

  export default {
    props: ["deals", "fields", "pageSize"],
    data() {
      return {
        currentPage: 1,
        sortField: "id",
        sortAscending: true,
        fieldNameMap: {
          country: "Target country",
          top_investors: "Top investors",
          intention_of_investment: "Intention of investment",
          current_negotiation_status: "Negotiation status",
          current_implementation_status: "Implementation status",
          deal_size: "Deal size in ha",
          fully_updated: "Full updated",
          status: "Status",
          draft_status: "Draft status",
          confidential: "Confidential",
          operating_company: "Operating company",
          created_at: "Created at",
          modified_at: "Last modified at",
          fully_updated_at: "Fully updated at",
          cached_has_no_known_investor: "Has no known investor"
        },
      };
    },
    computed: {
      pages() {
        if (this.deals.length > 0) {
          return Math.ceil(this.deals.length / parseInt(this.pageSize));
        }
        return 0;
      },
      dt_deals() {
        let deals = sortAnything(this.deals, this.sortField, this.sortAscending);

        if (this.pageSize) {
          return deals.slice(
            this.pageSize * (this.currentPage - 1),
            this.pageSize * this.currentPage
          );
        }
        return deals;
      },
    },
    methods: {
      setSort(field) {
        if (this.sortField === field) this.sortAscending = !this.sortAscending;
        this.sortField = field;
      },
      displayField(deal, field) {
        let val = deal[field];
        if (field === "status") {
          return STATUS_MAP[val];
        } else if (field === "draft_status") {
          return DRAFT_STATUS_MAP[val];
        } else {
          return val;
        }
      },
      parseTopInvestors(deal) {
        if (!deal.top_investors) return "";
        return deal.top_investors
          .map((inv) => {
            return inv.name;
          })
          .join("<br>");
      },
      parseIntentionOfInvestment(deal) {
        if (!deal.intention_of_investment) return "";
        return deal.intention_of_investment
          .map((int) => {
            let intention = int.value;
            console.log(int);
            let slug = intention; //slugify(intention, { lower: true });
            return `<a href="/data/by-intention/${intention}/"
                      class="toggle-tooltip intention-icon ${slug}" title=""
                      data-original-title="${intention}"><span>${intention}</span></a>`;
          })
          .sort();
      },
    },
  };
</script>

<style scoped lang="scss">
  @import "../../scss/colors";

  a.page-link:not([href]) {
    color: var(--primary);
  }
  .page-item.disabled .page-link {
    color: #6c757d;
  }

  th.selected {
    font-weight: 600;
    color: var(--primary);

    &.asc:before {
      content: "\f078";
      font-family: "Font Awesome 5 Free";
    }

    &:not(.asc):before {
      content: "\f077";
      font-family: "Font Awesome 5 Free";
    }
  }
</style>
