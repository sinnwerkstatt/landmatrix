<template>
  <div>
    <div v-for="section in sections" class="panel-body">
      <h3>{{ section.name }}</h3>
      <div
        v-for="formfield in section.fields"
        :key="formfield.name"
        :class="['row', 'mt-3', formfield.name]"
        v-if="deal[formfield.name] || !readonly"
      >
        <div class="col-md-3">
          {{ formfield.label }}
        </div>
        <div class="col-md-9">
          <component
            :is="formfield.component"
            :formfield="formfield"
            :readonly="!!readonly"
            v-model="deal[formfield.name]"
          ></component>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import TextField from "@/components/Fields/TextField";
  import ValueDateField from "@/components/Fields/ValueDateField";
  import CheckboxField from "@/components/Fields/CheckboxField";

  export default {
    props: ["sections", "deal", "readonly"],
    components: { TextField, ValueDateField, CheckboxField },
  };
</script>
