<template>
  <b-tab :title="$t(title)" :active="active" @click="$emit('activated')">
    <div v-for="section in sections" :key="section.name" class="panel-body">
      <h3>{{ $t(section.name) }}</h3>
      <EditField
        v-for="fieldname in section.fields"
        :key="fieldname"
        v-model="deal[fieldname]"
        :fieldname="fieldname"
      />
    </div>

    <slot />
  </b-tab>
</template>

<script>
  import EditField from "$components/Fields/EditField";

  export default {
    name: "DealEditSection",
    components: { EditField },
    props: {
      title: { type: String, required: true },
      sections: { type: Array, required: true },
      deal: { type: Object, required: true },
      active: { type: Boolean, default: false }
    },
    computed: {},
    methods: {}
  };
</script>

<style lang="scss" scoped>
  .display-field-wrapper {
    margin-top: 2em;
  }

  .panel-body {
    background-color: rgba(200, 200, 200, 0.1);
    background-image: linear-gradient(to bottom, rgba(200, 200, 200, 0.04), rgba(200, 200, 200, 0.1));
    margin-left: -15px;
    margin-right: -15px;
    padding: 15px;
    border-radius: 5px;
    margin-bottom: 0.5em;
    border-bottom: 1px solid rgba(200, 200, 200, 0.3);

    > h3:first-child {
      margin-top: 0;
    }
  }
</style>
