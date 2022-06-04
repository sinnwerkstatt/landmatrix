<template>
  <FilterCollapse
    :title="$t('Negotiation status').toString()"
    :clearable="negotiation_status.length > 0"
    @click="negotiation_status = []"
  >
    <div v-for="nstat in choices" :key="nstat.value">
      <div v-if="nstat.group" class="custom-control custom-checkbox">
        <input
          :id="nstat.group"
          v-model="nstat.state"
          class="custom-control-input"
          type="checkbox"
          @change="toggleGroup(nstat)"
        />
        <label
          class="custom-control-label orange-checkbox-label font-weight-bold"
          :for="nstat.group"
        >
          {{ $t(nstat.group) }}
        </label>
        <div
          v-for="nstatop in nstat.options"
          :key="nstatop.value"
          class="custom-control custom-checkbox"
        >
          <input
            :id="nstatop.value"
            v-model="negotiation_status"
            class="form-check-input custom-control-input"
            type="checkbox"
            :value="nstatop.value"
            @change="toggleSingle(nstat)"
          />
          <label class="form-check-label custom-control-label" :for="nstatop.value">
            {{ $t(nstatop.name) }}
          </label>
        </div>
      </div>
      <div v-else class="custom-control custom-checkbox font-weight-bold">
        <input
          :id="nstat.value"
          v-model="negotiation_status"
          class="form-check-input custom-control-input"
          type="checkbox"
          :value="nstat.value"
        />
        <label class="form-check-label custom-control-label" :for="nstat.value">
          {{ $t(nstat.name) }}
        </label>
      </div>
    </div>
  </FilterCollapse>
</template>

<script lang="ts">
  import FilterCollapse from "$components/Data/FilterCollapse.vue";
  import Vue from "vue";

  interface Choice {
    group?: string;
    state?: boolean;
    value?: string;
    name?: string;
  }
  interface GroupChoice extends Choice {
    group: string;
    options: { value: string; name: string }[];
  }
  function isSuperset(set: Set<string>, subset: Set<string>): boolean {
    for (let elem of subset) {
      if (!set.has(elem)) {
        return false;
      }
    }
    return true;
  }

  function hasIntersection(setA: Set<string>, setB: Set<string>): boolean {
    for (let elem of setB) {
      if (setA.has(elem)) return true;
    }
    return false;
  }

  export default Vue.extend({
    components: { FilterCollapse },

    data() {
      return {
        choices: [
          {
            group: "Intended",
            state: undefined,
            options: [
              { value: "EXPRESSION_OF_INTEREST", name: "Expression of interest" },
              { value: "UNDER_NEGOTIATION", name: "Under negotiation" },
              {
                value: "MEMORANDUM_OF_UNDERSTANDING",
                name: "Memorandum of understanding",
              },
            ],
          },
          {
            group: "Concluded",
            state: undefined,
            options: [
              { value: "ORAL_AGREEMENT", name: "Oral agreement" },
              { value: "CONTRACT_SIGNED", name: "Contract signed" },
              { value: "CHANGE_OF_OWNERSHIP", name: "Change of ownership" },
            ],
          },
          {
            group: "Failed",
            state: undefined,
            options: [
              { value: "NEGOTIATIONS_FAILED", name: "Negotiations failed" },
              { value: "CONTRACT_CANCELED", name: "Contract cancelled" },
            ],
          },
          { value: "CONTRACT_EXPIRED", name: "Contract expired" },
        ] as Choice[],
      };
    },
    computed: {
      negotiation_status: {
        get() {
          return this.$store.state.filters.negotiation_status;
        },
        set(value) {
          if (value !== this.$store.state.filters.negotiation_status) {
            this.$store.dispatch("setFilter", { filter: "negotiation_status", value });
          }
        },
      },
    },
    watch: {
      "$store.state.signalNegstat"() {
        this.choices.forEach((choice) => {
          if (choice.group) this.toggleSingle(choice as GroupChoice);
        });
      },
    },
    mounted() {
      this.choices.forEach((choice) => {
        if (choice.group) this.toggleSingle(choice as GroupChoice);
      });
    },
    methods: {
      toggleGroup(choice: GroupChoice) {
        // const fieldmap: { [key: string]: string[] } = {
        //   Concluded: ["ORAL_AGREEMENT", "CONTRACT_SIGNED"],
        // };
        const fields = choice.options.map((o) => o.value);

        if (choice.state) {
          this.negotiation_status = [...this.negotiation_status, ...fields];
        } else {
          this.negotiation_status = this.negotiation_status.filter(
            (s: string) => !fields.includes(s)
          );
        }
      },
      toggleSingle(choice: GroupChoice) {
        const cur_set: Set<string> = new Set(this.negotiation_status);
        const exp_set: Set<string> = new Set(choice.options.map((o) => o.value));
        const checkbox = document.getElementById(choice.group) as HTMLInputElement;

        if (isSuperset(cur_set, exp_set)) {
          checkbox.indeterminate = false;
          choice.state = true;
        } else if (hasIntersection(cur_set, exp_set)) {
          checkbox.indeterminate = true;
        } else {
          checkbox.indeterminate = false;
          choice.state = false;
        }
      },
    },
  });
</script>
