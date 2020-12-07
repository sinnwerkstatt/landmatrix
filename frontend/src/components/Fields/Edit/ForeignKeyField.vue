<template>
  <div class="form-field row">
    <div class="label" :class="labelClasses">
      {{ formfield.label }}
    </div>
    <div class="val" :class="valClasses">
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
  import { fieldMixin } from "./fieldMixin";

  export default {
    mixins: [fieldMixin],
  };
</script>
