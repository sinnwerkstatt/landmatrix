<template>
  <div class="investor-table">
    <nav aria-label="Investor table navigation">
      <ul class="pagination justify-content-center" v-if="pages > 1">
        <li
          v-for="(n, i) in pages"
          class="page-item"
          :class="['page-item', currentPage === i ? 'disabled' : '']"
        >
          <a class="page-link" @click="currentPage = i">{{ i + 1 }}</a>
        </li>
      </ul>
    </nav>

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
        <tr v-for="data in dt_data" :key="data.id">
          <td>
            <router-link
              :to="{ name: 'investor_detail', params: { investor_id: data.id } }"
              v-slot="{ href }"
            >
              <a :href="href">{{ data.id }}</a>
            </router-link>
          </td>
          <td v-for="field in fields" :key="field" v-html="data[field]"></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  const slugify = require("slugify");

  export default {
    props: ["investors", "fields", "pageSize"],
    data() {
      return {
        currentPage: 0,
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
        },
      };
    },
    computed: {
      pages() {
        if (this.investors.length > 0) {
          return Math.ceil(this.investors.length / parseInt(this.pageSize));
        }
        return 0;
      },
      dt_data() {
        let sfield = this.sortField;
        let sasc = this.sortAscending;
        function sortAnything(a, b) {
          let fieldx = sasc ? a[sfield] : b[sfield];
          let fieldy = sasc ? b[sfield] : a[sfield];

          let field_type = typeof fieldx;
          if (field_type === typeof "") {
            return fieldx.localeCompare(fieldy);
          }
          return fieldy - fieldx;
        }
        let investors = this.investors.sort(sortAnything);

        if (this.pageSize) {
          return investors.slice(
            this.pageSize * this.currentPage,
            this.pageSize * (this.currentPage + 1)
          );
        }
        return investors;
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

<style scoped lang="scss">
  @import "../../scss/colors";

  a.page-link:not([href]) {
    color: $lm_investor;
  }
  .page-item.disabled .page-link {
    color: #6c757d;
  }

  th.selected {
    font-weight: 600;
    color: $lm_investor;

    &.asc:before {
      content: "\f078";
      font-family: FontAwesome;
    }

    &:not(.asc):before {
      content: "\f077";
      font-family: FontAwesome;
    }
  }
</style>
