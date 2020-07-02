<template>
  <div>
    <div v-for="section in sections" class="panel-body">
      <h3>{{ section.name }}</h3>
      <dl
        v-for="formfield in section.fields"
        :key="formfield.name"
        :class="['row', 'mt-3', formfield.name]"
        v-if="!readonly || (deal[formfield.name] !== undefined) "
      >
        <dt class="col-md-3">
          {{ formfield.label }}
        </dt>
        <dd class="col-md-9">
          <component
            :is="formfield.component"
            :formfield="formfield"
            :readonly="!!readonly"
            v-model="deal[formfield.name]"
          ></component>
        </dd>
      </dl>
    </div>
  </div>
</template>

<script>
  import BooleanField from "@/components/Fields/BooleanField";
  import CheckboxField from "@/components/Fields/CheckboxField";
  import DecimalField from "@/components/Fields/DecimalField";
  import ForeignKeyField from "@/components/Fields/ForeignKeyField";
  import TextField from "@/components/Fields/TextField";
  import ValueDateField from "@/components/Fields/ValueDateField";

  export default {
    props: ["sections", "deal", "readonly"],
    components: {
      BooleanField,
      CheckboxField,
      DecimalField,
      ForeignKeyField,
      TextField,
      ValueDateField,
    },
  };
</script>
