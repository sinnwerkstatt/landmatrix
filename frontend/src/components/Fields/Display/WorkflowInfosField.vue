<template>
  <div>
    {{ value[0].timestamp | dayjs("YYYY-MM-DD") }}<br />
    <div>
      <span> From {{ value[0].from_user.username }}</span>
      <span v-if="value[0].to_user"> to {{ value[0].to_user.username }}</span>
    </div>
    {{ value[0].comment }}
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Array, required: true },
      model: { type: String, required: true },
    },
    methods: {},
  };
</script>
