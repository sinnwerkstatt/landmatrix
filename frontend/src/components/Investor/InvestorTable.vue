<template>
  <div class="investor-table">
    <b-pagination
      v-model="currentPage"
      :total-rows="investors.length"
      :per-page="pageSize"
      align="center"
      limit="12"
    ></b-pagination>
    <table id="summary" class="table table-striped">
      <thead>
        <tr>
          <th
            :class="{ selected: sortField === 'id', asc: sortAscending }"
            @click="setSort('id')"
          >
            #
          </th>
          <th
            v-for="field in fields"
            :key="field"
            :class="{ selected: sortField === field, asc: sortAscending }"
            @click="setSort(field)"
          >
            {{ fieldNameMap[field] || field }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="data in dt_data" :key="data.id">
          <td>
            <router-link
              v-slot="{ href }"
              :to="{ name: 'investor_detail', params: { investorId: data.id } }"
            >
              <a :href="href">{{ data.id }}</a>
            </router-link>
          </td>
          <td
            v-for="field in fields"
            :key="field"
            v-html="displayField(data, field)"
          ></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import { draft_status_map, status_map } from "$utils/choices";

  export default {
    props: ["investors", "fields", "pageSize"],
    data() {
      return {
        currentPage: 1,
        sortField: "id",
        sortAscending: true,
        fieldNameMap: {
          name: "Name",
          country: "Country of registration",
          top_investors: "Top investors",
          intention_of_investment: "Intention of investment",
          current_negotiation_status: "Negotiation status",
          current_implementation_status: "Implementation status",
          deal_size: "Deal size in ha",
          fully_updated: "Full updated",
          status: "Status",
          draft_status: "Draft status",
          created_at: "Created at",
          modified_at: "Last modified at",
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
        let investors = [...this.investors].sort(sortAnything);

        if (this.pageSize) {
          return investors.slice(
            this.pageSize * (this.currentPage - 1),
            this.pageSize * this.currentPage
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
      displayField(data, field) {
        let val = data[field];
        if (field === "status") {
          return status_map[val];
        } else if (field === "draft_status") {
          return draft_status_map[val];
        } else {
          return val;
        }
      },
    },
  };
</script>

<style scoped lang="scss">
  a.page-link:not([href]) {
    color: var(--color-lm-investor);
  }
  .page-item.disabled .page-link {
    color: #6c757d;
  }

  th.selected {
    font-weight: 600;
    color: var(--color-lm-investor);

    &.asc:before {
      content: "\f078";
      //noinspection CssNoGenericFontName
      font-family: "Font Awesome 5 Free";
    }

    &:not(.asc):before {
      content: "\f077";
      //noinspection CssNoGenericFontName
      font-family: "Font Awesome 5 Free";
    }
  }
</style>
