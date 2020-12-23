<template>
  <b-tab
    :title="title"
    v-if="entries.length"
    :active="active"
    @click="$emit('activated')"
  >
    <div class="row">
      <div :class="wrapperClasses">
        <div v-for="(entry, index) in entries" class="panel-body" :key="index">
          <h3>
            {{ model_name }} <small>#{{ index + 1 }}</small>
          </h3>
          <DisplayField
            v-for="fieldname in fields"
            :fieldname="fieldname"
            :value="entry[fieldname]"
            :model="model"
            :label_classes="label_classes"
            :value_classes="value_classes"
            :key="fieldname"
          />
        </div>
      </div>
      <slot></slot>
    </div>
  </b-tab>
</template>

<script>
  import DisplayField from "components/Fields/DisplayField";

  export default {
    props: [
      "title",
      "model",
      "model_name",
      "entries",
      "fields",
      "active",
      "label_classes",
      "value_classes",
    ],
    components: { DisplayField },
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
