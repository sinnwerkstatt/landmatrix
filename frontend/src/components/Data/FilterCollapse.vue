<template>
  <div class="filter-collapse">
    <div
      class="toggle"
      :class="{ active: clearable, collapsed: !initExpanded }"
      data-toggle="collapse"
      :data-target="'#' + slotId"
      :aria-expanded="initExpanded ? 'true' : 'false'"
    >
      <i class="expand-toggle fas fa-chevron-up"></i>
      <span class="title">{{ $t(title) }}</span>
      <span
        v-if="clearable"
        class="delete-button fa-stack"
        title="Remove this filter"
        @click.stop="$emit('click')"
      >
        <i class="fas fa-filter fa-stack-1x" />
        <i class="fas fa-circle fa-stack-1x fa-inverse"></i>
        <i class="far fa-circle fa-stack-1x"></i>
        <i class="fas fa-minus fa-stack-1x"></i>
      </span>
    </div>
    <div
      :id="slotId"
      class="expand-slot collapse"
      :class="{ show: initExpanded || false }"
    >
      <slot />
    </div>
  </div>
</template>
<script>
  export default {
    name: "FilterCollapse",
    props: {
      title: { type: String, required: true },
      clearable: { type: Boolean, default: false },
      initExpanded: { type: Boolean, default: false },
    },
    data() {
      return {
        shown: this.initExpanded || false,
      };
    },
    computed: {
      slotId() {
        return "slot" + this._uid;
      },
    },
  };
</script>

<style lang="scss">
  @import "../../scss/colors";

  .filter-collapse {
    margin-left: -0.5em;
    margin-right: -0.5em;
    padding: 5px 0.5em 0 0.5em;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);

    &:hover {
      cursor: pointer;
    }
    .toggle {
      padding-bottom: 5px;
      position: relative;
      &.active {
        color: $lm_orange;
      }
      .title {
        padding-right: 0;
      }
      .expand-toggle {
        color: rgba(0, 0, 0, 0.3);
        font-weight: bold;
        font-size: 12px;
        margin-right: 3px;
        transition: all 0.1s ease;
      }
      &.collapsed {
        .expand-toggle {
          transform: rotate(-180deg);
        }
      }
    }

    ul {
      padding-left: 0.3em;
      list-style: none;
    }

    .delete-button {
      position: absolute;
      font-weight: bold;
      font-size: 13px;
      top: -3px;
      right: -4px;
      opacity: 0.5;
      color: lighten($lm_orange, 5%);
      .fa-circle,
      .fa-minus {
        left: 8px;
        top: 5px;
      }
      .fa-circle {
        font-size: 0.9em;
        &.far {
          z-index: 1;
        }
      }
      .fa-minus {
        font-size: 0.5em;
      }
      &:hover {
        color: $lm_orange;
        opacity: 1;
      }
    }
    .expand-slot {
      box-shadow: inset 0 3px 7px -3px rgba(0, 0, 0, 0.1),
        inset 0px -2px 5px -2px rgba(0, 0, 0, 0.1);
      background-color: rgba(0, 0, 0, 0.01);
      padding: 0.5em 0.5em;
      margin: 0 -0.5em;
      transition: all 0.1s ease;
      > * {
        margin-bottom: 0;
      }
      font-size: 14px;
      .custom-radio {
        padding-left: 1.5em;
        .custom-control-label {
          &:before,
          &:after {
            width: 1em;
            height: 1em;
            top: 0.25em;
            left: -1.5em;
          }
          &:after {
            top: 0.2em;
            width: 0;
            height: 0;
            left: -1.53em;
          }
        }
      }
    }
  }
</style>
