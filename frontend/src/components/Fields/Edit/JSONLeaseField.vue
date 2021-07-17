<template>
  <div class="nowrap">
    <table class="w-100">
      <thead>
        <tr>
          <th>Current</th>
          <th>Date</th>
          <th>Area (ha)</th>
          <th>Farmers</th>
          <th>Households</th>
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
            <input
              v-model="val.farmers"
              type="number"
              class="form-control"
              :required="formfield.required"
              @input="updateEntries"
            />
          </td>
          <td>
            <input
              v-model="val.households"
              type="number"
              class="form-control"
              :required="formfield.required"
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
    computed: {
      filteredVals() {
        return this.vals.filter((x) => x.date || x.area || x.farmers || x.households);
      },
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
