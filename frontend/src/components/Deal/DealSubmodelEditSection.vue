<template>
  <b-tab :title="$t(title)" :active="active" @click="$emit('activated')">
    <div class="row">
      <div :class="wrapperClasses">
        <div v-for="(entry, index) in entries" :key="index" class="panel-body">
          <h3>
            {{ $t(modelName) }} <small>#{{ index + 1 }}</small>
            <button
              type="button"
              class="btn btn-secondary"
              @click="$emit('removeEntry', index)"
            >
              <i class="fa fa-minus"></i>
            </button>
          </h3>
          <EditField
            v-for="fieldname in fields"
            :key="fieldname"
            :fieldname="fieldname"
            v-model="entry[fieldname]"
            :model="model"
            :label-classes="labelClasses"
            :value-classes="valueClasses"
          />
        </div>
      </div>
      <slot />
    </div>
    <div class="mt-5 float-right">
      <button type="button" class="btn btn-primary" @click="$emit('addEntry')">
        <i class="fa fa-plus"></i> {{ $t(modelName) }}
      </button>
    </div>
  </b-tab>
</template>

<script>
  import EditField from "$components/Fields/EditField";

  export default {
    components: { EditField },
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
      wrapperClasses() {
        if (!!this.$slots.default) return ["col-md-12", "col-lg-7", "col-xl-6"];
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
