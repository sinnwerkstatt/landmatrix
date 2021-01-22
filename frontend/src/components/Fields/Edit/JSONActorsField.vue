<template>
  <div class="nowrap">
    <div v-for="(val, i) in vals" class="row">
      <div class="col-5">
        <input
          type="text"
          placeholder="Name"
          aria-label="Name"
          v-model="val.name"
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
      <div class="col-2">
        <a class="btn" @click.prevent="addEntry"><i class="fa fa-plus"></i></a>
        <a
          :class="{ disabled: vals.length <= 1 }"
          class="btn"
          @click.prevent="removeEntry(i)"
        >
          <i class="fa fa-minus"></i
        ></a>
      </div>
    </div>
  </div>
</template>

<script>
  import JSONFieldMixin from "../JSONFieldMixin";

  export default {
    mixins: [JSONFieldMixin],
    data() {
      return {
        vals: this.value ? this.value : [{ name: null, role: [] }],
      };
    },
    watch: {
      vals: {
        handler(newValue) {
          this.$emit("input", newValue);
        },
        deep: true,
      },
    },
    methods: {
      addEntry() {
        this.vals.push({ name: null, role: [] });
      },
      removeEntry(index) {
        this.vals.splice(index, 1);
      },
    },
  };
</script>
