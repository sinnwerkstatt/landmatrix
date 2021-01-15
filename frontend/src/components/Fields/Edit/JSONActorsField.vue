<template>
  <div class="nowrap">
    <div v-for="val in vals" class="row">
      <div class="col-5">
        <input
          type="text"
          placeholder="Name"
          aria-label="Name"
          :value="val.name"
          name="name"
          class="form-control"
        />
      </div>
      <div class="col-5">
        <select v-model="val.role" :name="formfield.name" class="form-control">
          <option value="">--------</option>
          <option v-for="(v, k) in formfield.choices" :key="k" :value="k">
            {{ v }}
          </option>
        </select>
      </div>
      <div class="col-2"><i class="fa fa-plus"></i> <i class="fa fa-minus"></i></div>
    </div>
  </div>
</template>

<script>
  import JSONField from "./JSONField";

  export default {
    mixins: [JSONField],
    data() {
      return {
        vals: this.value ? this.value : [{ name: null, role: [] }],
      };
    },
  };
</script>
