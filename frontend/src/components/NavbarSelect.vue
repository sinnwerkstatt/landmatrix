<template>
  <li class="nav-item dropdown" :class="{ showDropdown }">
    <a
      class="nav-link dropdown-toggle"
      id="navbarDropdown"
      role="button"
      aria-haspopup="true"
      aria-expanded="false"
      @click.capture="focusInputField"
    >
      {{ title }}
    </a>
    <div
      class="dropdown-menu"
      aria-labelledby="navbarDropdown"
      :class="{ hidden: !showDropdown }"
    >
      <input
        v-model="filterText"
        ref="inputField"
        type="text"
        @blur="loseFocus"
        @keydown.down="traverseList('down')"
        @keydown.up="traverseList('up')"
        @keyup.enter="emitSelect(selected)"
      />
      <ul>
        <li
          class="entries"
          v-for="option in _options"
          :key="option.id"
          @mousedown="emitSelect(option)"
          :class="{ selected: selected === option }"
        >
          {{ option.name }}
        </li>
      </ul>
    </div>
  </li>
</template>

<script>
  export default {
    props: ["title", "options"],
    data: function () {
      return {
        filterText: "",
        showDropdown: false,
        selected: null,
      };
    },
    computed: {
      _options() {
        if (this.options) {
          return this.options.filter((option) => {
            return (
              option.name.toLowerCase().includes(this.filterText.toLowerCase()) ||
              option.slug.toLowerCase().includes(this.filterText.toLowerCase())
            );
          });
        }
      },
    },
    methods: {
      traverseList(direction) {
        let val = direction === "down" ? 1 : -1;
        if (this.selected) {
          let index = this._options.indexOf(this.selected);
          this.selected = this._options[index + val];
        } else {
          this.selected = val === 1 ? this._options[0] : this._options.slice(-1)[0];
        }
      },
      loseFocus() {
        this.$nextTick(() => {
          this.filterText = "";
          this.showDropdown = false;
          this.selected = null;
        });
      },
      focusInputField() {
        this.showDropdown = true;
        if (this.showDropdown) {
          this.$nextTick(function () {
            this.$refs.inputField.focus();
          });
        }
      },
      emitSelect(option) {
        this.loseFocus();
        this.$emit("select", option);
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../scss/colors";

  li.showDropdown {
    background: white;
  }

  .nav-link {
    font-size: 18px;
    color: $lm_dark;
    padding: 15px;
  }

  ul {
    max-height: 200px;
    overflow-y: auto;
    list-style-type: none;
    padding: 0;
  }

  li.entries {
    cursor: pointer;
    &.selected {
      background: $primary;
    }
    &:hover {
      background: $primary;
    }
  }

  .dropdown-menu {
    &.hidden {
      display: none;
    }
    display: inline-block;
  }
</style>
