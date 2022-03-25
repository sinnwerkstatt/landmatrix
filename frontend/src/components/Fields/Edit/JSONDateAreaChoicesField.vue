<template>
  <div class="whitespace-nowrap">
    <table class="w-100">
      <thead>
        <tr>
          <th>{{ $t("Current") }}</th>
          <th>{{ $t("Date") }}</th>
          <th>{{ $t("Area (ha)") }}</th>
          <th>{{ $t("Choices") }}</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(val, i) in vals" :key="i" :class="{ 'is-current': val.current }">
          <td class="text-center" @click="updateCurrent(i)">
            <div class="form-check form-check-inline">
              <input
                :id="`${formfield.name}_current_${i}`"
                v-model="current"
                :name="`${formfield.name}_current`"
                :required="
                  vals.length > 0 && (vals[0].date || vals[0].area || vals[0].choices)
                "
                class="form-check-input"
                type="radio"
                :value="i"
              />
            </div>
          </td>
          <td>
            <LowLevelDateYearField
              v-model="val.date"
              :required="formfield.required"
              @input="updateEntries"
            />
          </td>
          <td>
            <LowLevelDecimalField
              v-model="val.area"
              :required="formfield.required"
              unit="ha"
              @input="updateEntries"
            />
          </td>

          <td>
            <multiselect
              v-model="val.choices"
              :options="options"
              :placeholder="formfield.placeholder"
              :group-select="true"
              :multiple="true"
              :group-values="formfield.with_categories ? 'options' : null"
              :group-label="formfield.with_categories ? 'category' : null"
              :custom-label="(x) => labels[x]"
              :close-on-select="false"
              select-label=""
              @input="updateEntries"
            />
          </td>

          <td class="buttons">
            <a class="btn" @click.stop="addEntry"><i class="fa fa-plus"></i></a>
            <a
              :class="{ disabled: vals.length <= 1 }"
              class="btn"
              @click.stop="removeEntry(i)"
            >
              <i class="fa fa-minus"></i
            ></a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  import JSONFieldMixin from "../JSONFieldMixin";
  import LowLevelDateYearField from "./LowLevelDateYearField";
  import LowLevelDecimalField from "./LowLevelDecimalField";

  export default {
    components: { LowLevelDateYearField, LowLevelDecimalField },
    mixins: [JSONFieldMixin],
    data() {
      return {
        options: [],
        labels: {},
      };
    },
    computed: {
      filteredVals() {
        return this.vals.filter((x) => x.date || x.area || x.choices);
      },
    },
    created() {
      if (this.formfield.with_categories) {
        this.options = Object.entries(this.formfield.choices).map(([k, v]) => {
          let newopts = Object.entries(v).map(([h, j]) => {
            this.labels[h] = this.$t(j);
            return h;
          });
          return { category: k, options: newopts };
        });
      } else {
        this.options = Object.entries(this.formfield.choices).map(([k, v]) => {
          this.labels[k] = this.$t(v);
          return k;
        });
      }
    },
  };
</script>

<style lang="scss" scoped>
  th {
    text-align: center;
  }
  td {
    padding: 0.4em;
  }
</style>
