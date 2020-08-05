<template>
  <b-tab :title="title" v-if="submodel.length" :active="active">
    <div class="row">
      <div class="col-lg-6 col-xs-12">
        <div v-for="entry in submodel" class="panel-body">
          <h3>{{ title }} #{{ entry.id }}</h3>
          <component
            :is="formfield.class"
            :formfield="formfield"
            :readonly="!!readonly"
            v-model="entry[formfield.name]"
            :file_not_public="entry.file_not_public"
            v-for="formfield in fields"
            v-if="!readonly || custom_is_null(entry[formfield.name])"
          />
        </div>
      </div>
      <slot></slot>
    </div>
  </b-tab>
</template>

<script>
  import BooleanField from "/components/Fields/BooleanField";
  import CharField from "/components/Fields/TextField";
  import TextField from "/components/Fields/TextField";
  import URLField from "/components/Fields/TextField";
  import DateField from "/components/Fields/TextField";
  import PointField from "/components/Fields/PointField";
  import IntegerField from "/components/Fields/DecimalField";
  import EmailField from "/components/Fields/TextField";
  import FileField from "/components/Fields/FileField";

  export default {
    props: ["title", "fields", "submodel", "readonly", "active"],
    components: {
      BooleanField,
      CharField,
      DateField,
      PointField,
      TextField,
      IntegerField,
      URLField,
      EmailField,
      FileField,
    },
    methods: {
      custom_is_null(field) {
        return !(
          field === undefined ||
          field === null ||
          field === "" ||
          (Array.isArray(field) && field.length === 0)
        );
      },
    },
  };
</script>
