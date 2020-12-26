<template>
  <div>
    <template v-if="formfield.related_model === 'Investor'">
      <template v-for="val in value">
        <router-link
          class="investor"
          target="_blank"
          :to="{ name: 'investor_detail', params: { investorId: val.id } }"
        >
          {{ val.name }} (#{{ val.id }})
        </router-link>
        <br />
      </template>
    </template>
    <template v-else>
      {{ value }}
    </template>
  </div>
</template>

<script>
  export default {
    name: "ManyToManyField",
    props: {
      formfield: { type: Object, required: true },
      value: { type: [Array, Object], required: true },
      model: { type: String, required: true },
    },
  };
</script>
