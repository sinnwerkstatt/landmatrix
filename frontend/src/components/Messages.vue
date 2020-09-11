<template>
  <div class="container" v-if="messages.length > 0">
    <div v-for="msg in messages" role="alert" class="alert" :class="map_level(msg)">
      <strong>{{ msg.title }}</strong>
      {{ msg.text }}
    </div>
  </div>
</template>
<script>
  export default {
    name: "Messages",
    computed: {
      messages() {
        return this.$store.state.page.messages;
      },
    },
    methods: {
      map_level(msg) {
        if (!msg.level) return "alert-info";
        if (msg.level === "error") return "alert-danger";
        return `alert-${msg.level}`;
      },
    },
  };
</script>
