<template>
  <div class="nowrap">
    <table class="w-100">
      <thead>
        <tr>
          <th>Current</th>
          <th>Date</th>
          <th>Choice</th>
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
              v-model="val.choice"
              :options="options"
              :placeholder="formfield.placeholder"
              :group-select="true"
              :custom-label="(x) => labels[x]"
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

  export default {
    components: { LowLevelDateYearField },
    mixins: [JSONFieldMixin],
    data() {
      return {
        current: -1,
        vals: this.value
          ? JSON.parse(JSON.stringify(this.value))
          : [{ date: null, choice: null, current: true }],
        options: [],
        labels: {},
      };
    },
    created() {
      if (this.value) {
        this.current = this.value.map((e) => e.current).indexOf(true);
      }

      this.options = Object.entries(this.formfield.choices).map(([k, v]) => {
        this.labels[k] = this.$t(v);
        return k;
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
          this.vals.filter((x) => x.current || x.date || x.choice)
        );
      },
      addEntry() {
        this.vals.push({ date: null, area: null, choice: null });
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
