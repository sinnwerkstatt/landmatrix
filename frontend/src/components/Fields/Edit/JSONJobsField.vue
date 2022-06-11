<template>
  <div class="whitespace-nowrap">
    <table class="w-100">
      <thead>
        <tr>
          <th>{{ $t("Current") }}</th>
          <th>{{ $t("Date") }}</th>
          <th>{{ $t("Jobs") }}</th>
          <th>{{ $t("Employees") }}</th>
          <th>{{ $t("Workers") }}</th>
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
                  vals.length > 0 &&
                  (vals[0].date || vals[0].jobs || vals[0].employees || vals[0].workers)
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
              v-model="val.jobs"
              :required="formfield.required"
              :decimals="0"
              :min-value="0"
              @input="updateEntries"
            />
          </td>
          <td>
            <LowLevelDecimalField
              v-model="val.employees"
              :required="formfield.required"
              :decimals="0"
              :min-value="0"
              @input="updateEntries"
            />
          </td>
          <td>
            <LowLevelDecimalField
              v-model="val.workers"
              :required="formfield.required"
              :decimals="0"
              :min-value="0"
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
        return this.vals.filter((x) => x.date || x.jobs || x.employees || x.workers);
      },
    },
  };
</script>
