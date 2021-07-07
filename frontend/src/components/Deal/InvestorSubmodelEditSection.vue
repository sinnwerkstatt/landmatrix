<template>
  <section>
    <form :id="id">
      <div class="row">
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
                {{ $t(modelName) }} <small>#{{ index + 1 }}</small>
              </h3>
              <a class="trashbin" @click="$emit('removeEntry', index)">
                <i class="fas fa-trash"></i>
              </a>
            </div>
            <div v-if="active_entry === entry" class="submodel-body">
              <div v-for="fieldname in fields" :key="fieldname">
                <EditField
                  v-model="entry[fieldname]"
                  :fieldname="fieldname"
                  model="involvement"
                  :label-classes="['display-field-value', 'col-md-3']"
                  :value-classes="['display-field-label', 'col-md-9']"
                />
              </div>
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

<script>
  import EditField from "$components/Fields/EditField";

  export default {
    name: "InvestorSubmodelEditSection",
    components: { EditField },
    props: {
      id: { type: String, required: true },
      title: { type: String, required: true },
      modelName: { type: String, required: true },
      entries: { type: Array, required: true },
      active: { type: Boolean, default: false },
    },
    data() {
      let fields = [
        "investor",
        "investment_type",
        "percentage",
        "loans_amount",
        "loans_currency",
        "loans_date",
      ];
      console.log(this.id);
      if (this.id === "parents") fields.push("parent_relation");
      fields.push("comment");
      return {
        active_entry: null,
        fields,
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
        this.$nextTick(() => {
          this.active_entry = this.entries[this.entries.length - 1];
        });
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../../scss/colors";

  h3 small {
    font-size: 70%;
    color: #777;
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
    color: $lm_orange;

    &:hover {
      cursor: pointer;
      color: lighten($lm_orange, 10%);
      text-decoration: none;
    }
  }
</style>
