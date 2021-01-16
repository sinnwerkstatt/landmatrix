<template>
  <div class="">
    {{ value }}
    {{ formfield }}
    <table>
      <thead>
        <tr>
          <th v-if="has_current">Current</th>
          <th>Date</th>
          <th>Size (ha)</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(val, i) in vals"
          :key="i"
          :class="{ 'is-current': val.current }"
          @click="current = i"
        >
          <td class="text-center">
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
              :aria-label="formfield.placeholder"
              placeholder="YYYY-MM-DD"
            />
          </td>
          <td>
            <template v-if="formfield.choices">
              <multiselect
                v-model="val.value"
                class="multiselect"
                :options="convert_to_options(formfield.choices)"
                :placeholder="formfield.placeholder"
                :group-select="true"
                :multiple="formfield.multiselect.multiple"
                :group-values="
                  formfield.multiselect && formfield.multiselect.with_categories
                    ? 'options'
                    : null
                "
                label="name"
                :group-label="
                  formfield.multiselect && formfield.multiselect.with_categories
                    ? 'category'
                    : null
                "
              />
              <!-- :close-on-select="!formfield.multiselect.multiple"-->
              <!-- track-by="value"-->
              <!-- :custom-label="(x) => labels[x]"-->
            </template>
            <template v-else>
              <input
                v-model="val.value"
                :type="formfield.type || `text`"
                :placeholder="formfield.placeholder"
                class="form-control year-based"
                :aria-label="formfield.placeholder"
              />
            </template>
          </td>

          <td>
            <a
              :class="{ disabled: vals.length <= 1 }"
              class="btn remove-ybd delete-row"
              @click.prevent="removeSet(i)"
            >
              <i class="lm lm-minus"></i
            ></a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: [Array, Object], required: false, default: null },
      model: { type: String, required: true },
    },
    data() {
      return {
        current: -1,
      };
    },
    computed: {
      has_current() {
        // console.log(this.formfield, this.formfield.has_current);
        return this.formfield.has_current ? this.formfield.has_current : true;
      },
      vals: {
        get() {
          return this.value || [{ date: null, value: null }];
        },
        set(val) {
          this.updateValue(val);
        },
      },
    },
    watch: {
      current() {
        this.updateValue();
      },
    },
    created() {
      if (this.value) {
        this.current = this.value.map((e) => e.current).indexOf(true);
      }
    },
    methods: {
      addSet() {
        this.vals.push({ date: null, value: null });
      },
      removeSet(index) {
        this.vals.splice(index, 1);
      },
      updateValue(val) {
        let relevant_val = val ? val : this.vals;
        let vals_with_current = relevant_val.map((v, i) => {
          let current = i === this.current ? { current: true } : {};
          delete v.current;
          return { ...v, ...current };
        });
        this.$emit("input", vals_with_current);
      },
      convert_to_options(choices) {
        // console.log(choices);
        let xx = Object.entries(choices).map(([k, v]) => {
          let newopts = Object.entries(v).map(([h, j]) => {
            return { name: j, value: h };
          });
          return { category: k, options: newopts };
        });
        // console.log(xx);
        return xx;
      },
    },
  };
</script>
<style lang="scss" scoped>
  @import "../../../scss/colors";

  .input-group {
    padding: 0.4em;
  }

  .is-current {
    font-weight: bold;
    background: rgba($primary, 0.5);
    border-radius: 3px;
  }

  .multiselect {
    width: 60%;
  }
</style>
