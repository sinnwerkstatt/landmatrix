<template>
  <div>
    <a href="#" @click="displayDeals = !displayDeals">{{ value.length }}</a>
    <span v-if="displayDeals" v-for="val in value">
      <br />
      <router-link :to="{ name: 'deal_detail', params: { deal_id: val.id } }">
        #{{ val.id }}
      </router-link>
    </span>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "model"],
    data() {
      return {
        displayDeals: false,
      };
    },
  };
</script>
