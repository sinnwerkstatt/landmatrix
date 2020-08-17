<template>
  <b-tab :title="title" v-if="entries.length" :active="active">
    <div class="row">
      <div class="col-lg-6 col-xs-12">
        <div v-for="entry in entries" class="panel-body">
          <h3>{{ title }} #{{ entry.id }}</h3>
          <Field
            :fieldname="fieldname"
            :readonly="!!readonly"
            v-model="entry[fieldname]"
            v-for="fieldname in fields"
            :model="model"
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
    props: ["title", "model", "entries", "fields", "readonly", "active"],
    components: { Field },
  };
</script>
