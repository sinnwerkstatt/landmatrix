<template>
  <div>
    <template v-if="formfield.related_model === 'Investor'" v-for="val in value">
      <router-link
        class="investor"
        target="_blank"
        :to="{ name: 'investor_detail', params: { investor_id: val.id } }"
      >
        {{ val.name }} (#{{ val.id }})
      </router-link>
      <br />
    </template>
    <template v-else>
      {{ value }}
    </template>
  </div>
</template>

<script>
  export default {
    name: "ManyToManyField",
    props: ["formfield", "value", "model"],
  };
</script>
