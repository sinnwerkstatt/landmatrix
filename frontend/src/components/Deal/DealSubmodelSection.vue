<template>
  <b-tab :title="title" v-if="entries.length" :active="active">
    <div class="row">
      <div :class="wrapperClasses">
        <div v-for="(entry, index) in entries" class="panel-body">
          <h3>
            {{ model_name }} <small>#{{ index + 1 }}</small>
          </h3>
          <Field
            :fieldname="fieldname"
            :readonly="!!readonly"
            v-model="entry[fieldname]"
            v-for="fieldname in fields"
            :model="model"
            :narrow="!!narrow"
          />
        </div>
      </div>
      <slot></slot>
    </div>
  </b-tab>
</template>

<script>
  import Field from "/components/Fields/Field";

  export default {
    props: [
      "title",
      "model",
      "model_name",
      "entries",
      "fields",
      "readonly",
      "active",
      "narrow",
    ],
    components: { Field },
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
