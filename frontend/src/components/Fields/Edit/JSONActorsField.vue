<template>
  <div class="nowrap">
    <div v-for="(val, i) in vals" class="row">
      <div class="col-5">
        <input
          v-model="val.name"
          type="text"
          placeholder="Name"
          aria-label="Name"
          class="form-control"
          @input="updateEntries"
        />
      </div>
      <div class="col-5">
        <select v-model="val.role" class="form-control" @change="updateEntries">
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
    methods: {
      updateEntries() {
        this.$emit(
          "input",
          this.vals.filter((x) => x.name || x.role)
        );
      },
      addEntry() {
        this.vals.push({});
      },
      removeEntry(index) {
        this.vals.splice(index, 1);
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../../../scss/colors";

  .row {
    margin-bottom: 1em;
    &:last-child {
      margin-bottom: 0;
    }
  }
  td {
    padding: 0.4em;
  }
</style>
