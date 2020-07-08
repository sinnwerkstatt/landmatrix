<template>
  <div>
    <div v-if="readonly">
      <div v-for="val in vals" v-html="parseValues(val)"></div>
    </div>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "readonly"],
    data() {
      return {
        current: 0,
        vals: [{ date: null, value: null }],
      };
    },
    computed: {},
    methods: {
      addSet() {
        this.vals.push({ date: null, value: null });
      },
      removeSet(index) {
        this.vals.splice(index, 1);
      },
      updateVals() {
        let vals_with_current = this.vals.map((val, i) => {
          let current = i === this.current ? { current: true } : {};
          return { value: val.value, date: val.date, ...current };
        });
        this.$emit("input", vals_with_current);
      },
      parseValues: function (value) {
        let ret = "";
        if (value.date) ret += `<span class="date">[${value.date}]</span> `;

        let choices = this.formfield.choices;
        if (choices) {
          let newchoices = {};
          for (let [key, value] of Object.entries(choices)) {
            if (typeof value == 'string') {
              newchoices[key] = value;
            } else {
              for (let [key, v] of Object.entries(value)) {
                newchoices[key] = v;
              }

            }
          }
          choices = newchoices;
        }

        if (value.value instanceof Array) {
          if (choices) {
            ret += value.value.map((v) => choices[v]).join(", ");
          } else ret += value.value.join(", ");
        } else {
          if (choices) ret += choices[value.value];
          else ret += value.value;
        }
        return ret;
      },
    },
    created() {
      if (this.value) {
        this.current = this.value.map((e) => e.current).indexOf(true);
        this.vals = this.value;
      }
    },
  };
</script>
<style lang="scss" scoped>
  @import "../../scss/colors";

  .input-group {
    padding: 0.4em;
  }

  .current-value {
    background: rgba($primary, 0.5);

    &::before {
      content: "Current";
      position: absolute;
      bottom: -5px;
      font-size: 0.7em;
    }
  }

  .multiselect {
    width: 60%;
  }
</style>
<style></style>
