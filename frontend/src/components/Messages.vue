<template>
  <div class="message-container" v-if="messages.length > 0">
    <div v-for="msg in messages" role="alert" class="alert" :class="map_level(msg)">
      <button type="button" class="close" aria-label="Close" @click="removeMessage(msg.id)">
        <span aria-hidden="true">&times;</span>
      </button>
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
      removeMessage(id) {
        this.$store.commit("setMessages", this.messages.filter(x => x.id != id));
      },
    },
  };
</script>
<style type="scss" scoped>
.message-container {
  position: absolute;
  top: 4em;
  left: 3em;
  right: 3em;
  z-index: 1000;
  opacity: 0.95;
}
</style>
