<template>
  <section v-if="entries.length">
    <div class="flex">
      <div :class="wrapperClasses">
        <div v-for="(entry, index) in entries" :key="index" class="panel-body">
          <h3>
            {{ index + 1 }}. {{ $t(modelName) }}
            <!--            <small class="font-mono">{{ entry.id }}</small>-->
          </h3>
          <template v-for="fieldname in fields">
            <DisplayField
              v-if="!custom_is_null(entry[fieldname])"
              :key="fieldname"
              :fieldname="fieldname"
              :value="entry[fieldname]"
              :model="model"
              :label-classes="labelClasses"
              :value-classes="valueClasses"
              :file-not-public="entry.file_not_public"
            />
          </template>
        </div>
      </div>
      <slot />
    </div>
  </section>
</template>

<script lang="ts">
  import DisplayField from "$components/Fields/DisplayField.vue";
  import { custom_is_null } from "$utils/data_processing";
  import Vue from "vue";

  export default Vue.extend({
    components: { DisplayField },
    props: {
      model: { type: String, required: true },
      modelName: { type: String, required: true },
      entries: { type: Array, required: true },
      fields: { type: Array, required: true },
      labelClasses: {
        type: Array,
        default: () => ["display-field-label", "col-md-5", "col-lg-4"],
      },
      valueClasses: {
        type: Array,
        default: () => ["display-field-value", "col-md-7", "col-lg-8"],
      },
    },
    data() {
      return {
        custom_is_null,
      };
    },
    computed: {
      wrapperClasses() {
        if (this.$slots.default) return ["col-md-12", "col-lg-7", "col-xl-6"];
        else return ["w-full"];
      },
    },
  });
</script>

<style lang="scss" scoped>
  h3 small {
    font-size: 70%;
    color: #777;
  }
</style>
