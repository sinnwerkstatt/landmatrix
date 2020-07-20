<template>
  <b-tab :title="title" v-if="submodel.length" :active="active">
    <div class="row">
      <div class="col">
        <div v-for="entry in submodel" class="panel-body">
          <h3>{{ title }} #{{ entry.id }}</h3>
          <dl class="row mt-3">
            <template
              v-for="formfield in fields"
              :class="formfield.name"
              v-if="!readonly || custom_is_null(entry[formfield.name])"
            >
              <dt class="col-md-3" :key="`dt-${formfield.name}`">
                {{ formfield.label }}
              </dt>
              <dd class="col-md-9" :key="`dd-${formfield.name}`">
                <component
                  :is="formfield.class"
                  :formfield="formfield"
                  :readonly="!!readonly"
                  v-model="entry[formfield.name]"
                ></component>
              </dd>
            </template>
          </dl>
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
  import FileField from "/components/Fields/TextField";

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
