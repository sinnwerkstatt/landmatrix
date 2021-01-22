<template>
  <div class="nowrap">
    <table>
      <thead>
        <tr>
          <th>Current</th>
          <th>Date</th>
          <th>Area (ha)</th>
          <th>Choices</th>
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
            <input
              v-model="val.date"
              type="text"
              class="form-control year-based-year"
              placeholder="YYYY-MM-DD"
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
            <multiselect
              v-model="val.choices"
              class="multiselect"
              @input="updateEntries"
              :options="options"
              :placeholder="formfield.placeholder"
              :group-select="true"
              :multiple="formfield.multiselect && formfield.multiselect.multiple"
              :group-values="
                formfield.multiselect && formfield.multiselect.with_categories
                  ? 'options'
                  : null
              "
              :group-label="
                formfield.multiselect && formfield.multiselect.with_categories
                  ? 'category'
                  : null
              "
              :custom-label="(x) => labels[x]"
            />
            <!-- :close-on-select="!formfield.multiselect.multiple"-->
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
  import LowLevelDecimalField from "./LowLevelDecimalField";

  export default {
    components: { LowLevelDecimalField },
    mixins: [JSONFieldMixin],
    data() {
      return {
        current: -1,
        vals: this.value
          ? JSON.parse(JSON.stringify(this.value))
          : [{ date: null, area: null, choices: [], current: true }],
        options: [],
        labels: {},
      };
    },
    created() {
      if (this.value) {
        this.current = this.value.map((e) => e.current).indexOf(true);
      }
      this.options = Object.entries(this.formfield.choices).map(([k, v]) => {
        let newopts = Object.entries(v).map(([h, j]) => {
          this.labels[h] = this.$t(j);
          return h;
        });
        return { category: k, options: newopts };
      });
    },
    // computed: {
    //   options() {
    //
    //     console.log(xx);
    //     return xx;
    //   }
    // },
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
          this.vals.filter((x) => x.current || x.date || x.area || x.choices)
        );
      },
      addEntry() {
        // this.current = this.vals.length;
        this.vals.push({ date: null, area: null, choices: [] });
        this.updateEntries();
      },
      removeEntry(index) {
        this.current = Math.min(this.current, this.vals.length - 2);
        this.vals.splice(index, 1);
        this.updateEntries();
      },

      // convert_to_options(choices) {
      //   console.log(choices);
      //   let xx = Object.entries(choices).map(([k, v]) => {
      //     let newopts = Object.entries(v).map(([h, j]) => {
      //       return h;
      //     });
      //     return { category: k, options: newopts };
      //   });
      //   console.log(xx);
      //   return xx;
      // },
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
