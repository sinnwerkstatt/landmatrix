<template>
  <div class="row my-1">
    <div class="col-md-3 font-weight-bold">
      {{ formfield.label }}
    </div>
    <div class="col-md-9">
      <router-link
        v-if="formfield.related_model === 'Investor'"
        :to="{ name: 'investor_detail', params: { investor_id: val.id } }"
        v-slot="{ href }"
      >
        <a :href="href">{{ val.name }} (#{{ val.id }})</a>
      </router-link>
      <template v-else>
        {{ val.name }}
      </template>
    </div>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "readonly"],
    data() {
      return {
        val: this.value,
      };
    },
    methods: {
      emitVal() {
        this.$emit("input", this.val);
      },
    },
  };
</script>
