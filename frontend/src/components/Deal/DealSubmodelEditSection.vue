<template>
  <section>
    <form :id="id">
      <div class="flexwrap">
        <div :class="wrapperClasses">
          <div v-for="(entry, index) in entries" :key="index" class="panel-body">
            <div class="submodel-header">
              <i
                class="expand-toggle fas fa-chevron-down"
                :class="{
                  'fa-chevron-up': active_entry === entry,
                  'fa-chevron-down': active_entry !== entry,
                }"
                @click="active_entry = active_entry !== entry ? entry : null"
              ></i>
              <h3 @click="active_entry = active_entry !== entry ? entry : null">
                {{ $t(modelName) }} <small>#{{ entry.id }}</small>
              </h3>
              <a class="trashbin" @click="$emit('removeEntry', index)">
                <i class="fas fa-trash"></i>
              </a>
            </div>
            <div v-if="active_entry === entry" class="submodel-body">
              <EditField
                v-for="fieldname in fields"
                :key="fieldname"
                v-model="entry[fieldname]"
                :fieldname="fieldname"
                :model="model"
                :label-classes="['display-field-label', 'col-md-5', 'col-lg-4']"
                :value-classes="['display-field-value', 'col-md-7', 'col-lg-8']"
              />
            </div>
          </div>
        </div>
        <slot />
      </div>
      <div class="mt-3">
        <button type="button" class="btn btn-secondary" @click="add_entry">
          <i class="fa fa-plus"></i> {{ $t("Add " + modelName) }}
        </button>
      </div>
    </form>
  </section>
</template>

<script lang="ts">
  import EditField from "$components/Fields/EditField.vue";
  import Vue from "vue";

  export default Vue.extend({
    components: { EditField },
    props: {
      id: { type: String, required: true },
      model: { type: String, required: true },
      modelName: { type: String, required: true },
      entries: { type: Array, required: true },
      fields: { type: Array, required: true },
      active: { type: Boolean, default: false },
    },
    data() {
      return {
        active_entry: null,
      };
    },
    computed: {
      wrapperClasses() {
        if (this.$slots.default) return ["col-md-12", "col-lg-7", "col-xl-6"];
        else return ["col-12"];
      },
    },
    methods: {
      add_entry() {
        this.$emit("addEntry");
        this.active_entry = this.entries[this.entries.length - 1];
      },
    },
  });
</script>

<style lang="scss" scoped>
  section {
    margin-top: 2rem;
  }
  .flexwrap {
    display: flex;
    flex-wrap: wrap;
  }

  .submodel-header {
    display: flex;
    align-items: center;

    .expand-toggle {
      &:hover {
        cursor: pointer;
      }
    }

    h3 {
      margin: 0;

      &:hover {
        cursor: pointer;
      }

      small {
        font-size: 70%;
        color: #777;
      }
    }

    margin-bottom: 1em;

    & .expand-toggle {
      margin-right: 0.5em;
    }
  }

  .submodel-body {
    margin-bottom: 2em;
  }

  .fa-plus {
    margin-right: 0.3em;
  }

  .trashbin {
    margin-left: 2em;
    color: var(--color-lm-orange);

    &:hover {
      cursor: pointer;
      color: var(--color-lm-orange-light);
      text-decoration: none;
    }
  }
</style>
