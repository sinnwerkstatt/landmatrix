<template>
  <b-modal v-model="visible" :title="`${investor.name} (#${investor.id})`">
xxx
    <Field
      :fieldname="fieldname"
      :readonly="true"
      v-model="investor[fieldname]"
      v-for="fieldname in fields"
      model="investor"
    />

    <div v-if="investor.involvement">
      <h2>Involvement</h2>
      <Field
        :fieldname="fieldname"
        :readonly="true"
        v-model="investor.involvement[fieldname]"
        v-for="fieldname in involvement_fields"
        model="involvement"
      />
      {{ investor.involvement }}
    </div>
    <template v-slot:modal-footer>
      <div class="w-100">
        <router-link
          :to="{
            name: 'investor_detail',
            params: { investor_id: investor.id },
          }"
          class="btn btn-investor investor-link float-right"
          target="_blank"
          v-slot="{ href }"
        >
          <a :href="href">More details about this investor</a>
        </router-link>
      </div>
    </template>
  </b-modal>
</template>

<script>
  import Field from "/components/Fields/Field";

  export default {
    props: ["investor", "value"],
    components: { Field },
    data() {
      return {
        fields: ["classification", "country", "homepage", "comment"],
        involvement_fields: ["role"],
      };
    },
    computed: {
      visible: {
        get() {
          return this.value;
        },
        set(val) {
          this.$emit("input", val);
        },
      },
    },
  };
</script>
