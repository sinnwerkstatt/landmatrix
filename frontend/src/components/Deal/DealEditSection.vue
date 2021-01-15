<template>
  <b-tab :title="$t(title)" :active="active" @click="$emit('activated')">
    <div v-for="section in sections" :key="section.name" class="panel-body">
      <h3>{{ $t(section.name) }}</h3>
      <EditField
        v-for="fieldname in section.fields"
        :key="fieldname"
        :fieldname="fieldname"
        v-model="deal[fieldname]"
      />
    </div>

    <slot />
  </b-tab>
</template>

<script>
  import EditField from "components/Fields/EditField";

  export default {
    name: "DealEditSection",
    components: { EditField },
    props: {
      title: { type: String, required: true },
      sections: { type: Array, required: true },
      deal: { type: Object, required: true },
      active: { type: Boolean, default: false },
    },
    computed: {},
    methods: {},
  };
</script>
