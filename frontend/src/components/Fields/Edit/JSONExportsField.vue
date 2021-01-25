<template>
  <div class="nowrap">
    {{ vals }}
    {{ value }}
    <table class="w-100">
      <thead>
        <tr>
          <th>Current</th>
          <th>Date</th>
          <th>Choices</th>
          <th>Area (ha)</th>
          <th>Yield (tons)</th>
          <th>Export (%)</th>
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
                class="form-check-input"
                type="radio"
                :name="`${formfield.name}_current`"
                :value="i"
              />
            </div>
          </td>
          <td>
            <LowLevelDateYearField
              v-model="val.date"
              :name="formfield.name"
              :required="formfield.required"
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
              @input="updateEntries"
            />
          </td>
          <td>
            <LowLevelDecimalField
              v-model="val.area"
              :name="formfield.name"
              :required="formfield.required"
              unit="ha"
              @input="updateEntries"
            />
          </td>
          <td>
            <LowLevelDecimalField
              v-model="val.yield"
              :name="formfield.name"
              :required="formfield.required"
              unit="tons"
              @input="updateEntries"
            />
          </td>
          <td>
            <LowLevelDecimalField
              v-model="val.export"
              :name="formfield.name"
              :required="formfield.required"
              unit="%"
              @input="updateEntries"
            />
          </td>

          <td>
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
        current: -1,
        vals:
          this.value && this.value.length > 0
            ? JSON.parse(JSON.stringify(this.value))
            : [
                {
                  date: null,
                  choices: [],
                  area: null,
                  yield: null,
                  export: null,
                  current: true,
                },
              ],
        options: [],
        labels: {},
      };
    },
    created() {
      if (this.value) {
        this.current = this.value.map((e) => e.current).indexOf(true);
      }
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
    methods: {
      updateCurrent(i) {
        this.current = i;
        this.updateEntries();
      },
      updateEntries() {
        this.vals = this.vals.map((v, i) => {
          let current = i === this.current ? { current: true } : {};
          delete v.current;
          return { ...v, ...current };
        });
        this.$emit(
          "input",
          this.vals.filter(
            (x) => x.current || x.date || x.area || x.yield || x.export || x.choices
          )
        );
      },
      addEntry() {
        this.vals.push({
          date: null,
          choices: [],
          area: null,
          yield: null,
          export: null,
        });
        this.updateEntries();
      },
      removeEntry(index) {
        this.current = Math.min(this.current, this.vals.length - 2);
        this.vals.splice(index, 1);
        this.updateEntries();
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../../../scss/colors";

  th {
    text-align: center;
  }
  td {
    padding: 0.4em;
  }

  .is-current {
    font-weight: bold;
    background: rgba($primary, 0.5);
    border-radius: 3px;
  }
</style>
