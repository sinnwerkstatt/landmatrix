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
            <FieldLabel :fieldname="field" model="deal" :label-classes="[]" />
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="deal in dt_deals" :key="deal.id">
          <td>
            <router-link
              v-slot="{ href }"
              :to="{ name: 'deal_detail', params: { dealId: deal.id } }"
            >
              <a :href="href">{{ deal.id }}</a>
            </router-link>
          </td>
          <td v-for="field in fields" :key="field">
            <DisplayField :fieldname="field" :value="deal[field]" :show-label="false" />
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
  import { sortAnything } from "$utils";
  import Vue, { PropType } from "vue";
  import DisplayField from "$components/Fields/DisplayField.vue";
  import FieldLabel from "$components/Fields/FieldLabel.vue";
  import type { Deal } from "$types/deal";

  export default Vue.extend({
    components: { FieldLabel, DisplayField },
    props: {
      deals: { type: Array as PropType<Deal[]>, required: true },
      fields: { type: Array as PropType<Array<string>>, required: true },
      pageSize: { type: Number, default: null },
    },

    data() {
      return {
        currentPage: 1,
        sortField: "id",
        sortAscending: true,
      };
    },
    computed: {
      pages(): number {
        if (this.deals.length > 0) {
          return Math.ceil(this.deals.length / +this.pageSize);
        }
        return 0;
      },
      dt_deals(): Deal[] {
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
      setSort(field: string) {
        if (this.sortField === field) this.sortAscending = !this.sortAscending;
        this.sortField = field;
      },
    },
  });
</script>

<style scoped lang="scss">
  a.page-link:not([href]) {
    color: var(--color-lm-orange);
  }
  .page-item.disabled .page-link {
    color: #6c757d;
  }

  th.selected {
    font-weight: 600;
    color: var(--color-lm-orange);

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
