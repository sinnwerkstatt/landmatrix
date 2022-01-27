<template>
  <div class="whitespace-nowrap">
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
                :name="`${formfield.name}_current`"
                :required="vals.length > 0 && (vals[0].date || vals[0].choice)"
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
            <multiselect
              v-model="val.choice"
              :options="options"
              :placeholder="formfield.placeholder"
              :group-select="true"
              :custom-label="(x) => labels[x]"
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

  export default {
    components: { LowLevelDateYearField },
    mixins: [JSONFieldMixin],
    data() {
      return {
        options: [],
        labels: {},
      };
    },
    computed: {
      filteredVals() {
        return this.vals.filter((x) => x.date || x.choice);
      },
    },
    created() {
      this.options = Object.entries(this.formfield.choices).map(([k, v]) => {
        this.labels[k] = this.$t(v);
        return k;
      });
    },
  };
</script>
