<template>
  <div class="jsonjobs_field nowrap">
    <div v-for="val in vals" :class="{ 'font-weight-bold': val.current }">
      <span>{{ date_and_current(val) }}</span>
      <span v-if="val.jobs" class="mx-2">
        {{ val.jobs.toLocaleString("fr") }} jobs
      </span>
      <span v-if="val.employees" class="mx-2">
        {{ val.employees.toLocaleString("fr") }} employees
      </span>
      <span v-if="val.workers" class="mx-2">
        {{ val.workers.toLocaleString("fr") }} workers
      </span>
    </div>
  </div>
</template>

<script>
  import JSONFieldMixin from "../JSONFieldMixin";

  export default {
    mixins: [JSONFieldMixin],
    data() {
      return {
        vals: this.value ? this.value : [{ date: null, value: null }],
      };
    },
  };
</script>
