<template>
  <b-tab
    v-if="entries.length"
    :title="$t(title)"
    :active="active"
    @click="$emit('activated')"
  >
    <div class="row">
      <div :class="wrapperClasses">
        <div v-for="(entry, index) in entries" :key="index" class="panel-body">
          <h3>
            {{ $t(modelName) }} <small>#{{ index + 1 }}</small>
          </h3>
          <DisplayField
            v-for="fieldname in fields"
            :key="fieldname"
            :fieldname="fieldname"
            :value="entry[fieldname]"
            :model="model"
            :label-classes="labelClasses"
            :value-classes="valueClasses"
          />
        </div>
      </div>
      <slot />
    </div>
  </b-tab>
</template>

<script>
  import DisplayField from "components/Fields/DisplayField";

  export default {
    components: { DisplayField },
    props: {
      title: { type: String, required: true },
      model: { type: String, required: true },
      modelName: { type: String, required: true },
      entries: { type: Array, required: true },
      fields: { type: Array, required: true },
      active: { type: Boolean, default: false },
      labelClasses: {
        type: Array,
        default: () => ["display-field-label", "col-md-5", "col-lg-4"],
      },
      valueClasses: {
        type: Array,
        default: () => ["display-field-value", "col-md-7", "col-lg-8"],
      },
    },
    computed: {
      hasDefaultSlot() {
        return !!this.$slots.default;
      },
      wrapperClasses() {
        if (this.hasDefaultSlot) return ["col-md-12", "col-lg-7", "col-xl-6"];
        else return ["col-12"];
      },
    },
  };
</script>

<style lang="scss" scoped>
  h3 small {
    font-size: 70%;
    color: #777;
  }
</style>
