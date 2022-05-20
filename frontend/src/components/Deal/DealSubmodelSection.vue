<template>
  <section v-if="entries.length">
    <div class="flex">
      <div :class="wrapperClasses">
        <div
          v-for="(entry, index) in entries"
          :id="entry.id"
          :key="index"
          class="panel-body px-1 py-0.5"
          :class="
            nanoIDHighlight === entry.id ? 'bg-orange-100 animate-fadeToWhite' : ''
          "
        >
          <h3>{{ index + 1 }}. {{ $t(modelName) }}</h3>
          <DisplayField
            fieldname="id"
            :value="entry.id"
            :model="model"
            :label-classes="labelClasses"
            :value-classes="valueClasses"
          />

          <DisplayField
            v-for="fieldname in fields"
            v-if="!custom_is_null(entry[fieldname])"
            :key="fieldname"
            :fieldname="fieldname"
            :value="entry[fieldname]"
            :model="model"
            :label-classes="labelClasses"
            :value-classes="valueClasses"
            :file-not-public="entry.file_not_public"
          />
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
      return { custom_is_null };
    },
    computed: {
      nanoIDHighlight(): string {
        const [, nanoID] = this.$route.hash.split("/");
        return nanoID;
      },
      wrapperClasses() {
        if (this.$slots.default) return ["col-md-12", "col-lg-7", "col-xl-6"];
        else return ["w-full"];
      },
    },
    mounted() {
      if (this.nanoIDHighlight)
        document.getElementById(this.nanoIDHighlight)?.scrollIntoView();
    },
  });
</script>

<style lang="scss" scoped>
  h3 small {
    font-size: 70%;
    color: #777;
  }
</style>
