<template>
  <b-tab :title="title" v-if="submodel.length" :active="active">
    <div class="row">
      <div class="col-lg-6 col-xs-12">
        <div v-for="entry in submodel" class="panel-body">
          <h3>{{ title }} #{{ entry.id }}</h3>
          <Field
            :formfield="formfield"
            :readonly="!!readonly"
            v-model="entry[formfield.name]"
            :file_not_public="entry.file_not_public"
            v-for="formfield in fields"
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
    props: ["title", "fields", "submodel", "readonly", "active"],
    components: { Field },
  };
</script>
