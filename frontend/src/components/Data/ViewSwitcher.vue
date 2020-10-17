<template>
  <div class="viewswitcher">
    <div class="navbar navbar-expand">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link :to="{name:'map'}" class="nav-link">{{ $t("Map") }}</router-link>
        </li>
        <li class="nav-item dropdown">
          <a href=""
            class="nav-link dropdown-toggle"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
            id="viewswitch-data-dropdown"
            :class="{'router-link-active': isListRoute}"
          >{{ dataItemName }}</a>
          <span class="dropdown-menu">
            <router-link v-if="dataItemName!=label.deals" :to="{name:'list_deals'}" class="dropdown-item">{{ label.deals }}</router-link>
            <router-link v-if="dataItemName!=label.investors" :to="{name:'list_investors'}" class="dropdown-item">{{ label.investors }}</router-link>
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>


<script>
  export default {
    name: "ViewSwitcher",
    data() {
      return {
        label: {
          deals: this.$t("Deals"),
          investors: this.$t("Investors"),
        }
      };
    },
    computed: {
      isListRoute() {
        return ['list_deals', 'list_investors'].includes(this.$route.name);
      },
      dataItemName() {
        if (this.$route.name === "list_deals") {
          return this.label.deals;
        } else if (this.$route.name === "list_investors") {
          return this.label.investors;
        } else {
          return this.$t("Data");
        }
      }
    }
  }
</script>

<style lang="scss" scoped>
  @import "../../scss/colors";

  .viewswitcher {
    position: absolute;
    margin-left: auto;
    margin-right: auto;
    top: 10px;
    left: 0;
    right: 0;
    text-align: center;
    z-index: 1000;
    font-size: 0;
    filter: drop-shadow(3px 3px 3px rgba(0, 0, 0, 0.5));

    .navbar {
      justify-content: center;
      padding: 0;
      .nav-item {
        .nav-link {
          margin: 0;
          padding: 0.35em;
          width: 95px;
          text-align: center;
          background-color: white;
          color: black;
          font-size: 14px;
          font-weight: bold;
          &.router-link-active {
            background-color: $primary;
            color: white;
            &:hover {
              color: black;
            }
          }
          &:hover {
            color: $lm_orange;
          }
        }
        &.dropdown {
          .dropdown-menu {
            margin: 0;
            padding: 0;
            min-width: auto;
            border-radius: 0;
            width: 95px;
            border: none;
            .dropdown-item {
              margin: 0;
              padding: 0.35em 1em;
              font-weight: normal;
              &.router-link-exact-active {
                background-color: $primary;
                color: white;
              }
              &:hover {
                color: $lm_orange;
              }
            }
          }
        }
      }
      a {
        margin: 0;
        padding: 0.3em 2em;
        background-color: white;
        color: black;
        font-size: 14px;
        font-weight: bold;
        &.router-link-active {
          background-color: $primary;
          color: white;
        }
      }
    }

  }
</style>
