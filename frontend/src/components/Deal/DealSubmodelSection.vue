<template>
  <b-tab
    v-if="entries.length"
    :title="title"
    :active="active"
    @click="$emit('activated')"
  >
    <div class="row">
      <div :class="wrapperClasses">
        <div v-for="(entry, index) in entries" :key="index" class="panel-body">
          <h3>
            {{ modelName }} <small>#{{ index + 1 }}</small>
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
    props: [
      "title",
      "model",
      "modelName",
      "entries",
      "fields",
      "active",
      "labelClasses",
      "valueClasses",
    ],
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
