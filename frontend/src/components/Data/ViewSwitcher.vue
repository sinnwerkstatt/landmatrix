<template>
  <div class="viewswitcher">
    <div class="navbar navbar-expand">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link :to="{ name: 'map' }" class="nav-link">
            {{ $t("Map") }}
          </router-link>
        </li>
        <li class="nav-item dropdown">
          <a
            href=""
            class="nav-link dropdown-toggle"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
            id="viewswitch-data-dropdown"
            :class="{
              'router-link-active': isListRoute,
              investors: dataItemName === label.investors,
            }"
            >{{ dataItemName }}</a
          >
          <span class="dropdown-menu">
            <router-link
              v-if="dataItemName !== label.deals"
              :to="{ name: 'list_deals' }"
              class="dropdown-item deals"
              >{{ label.deals }}</router-link
            >
            <router-link
              v-if="dataItemName !== label.investors"
              :to="{ name: 'list_investors' }"
              class="dropdown-item investors"
              >{{ label.investors }}</router-link
            >
          </span>
        </li>
        <li class="nav-item dropdown">
          <a
            href=""
            class="nav-link dropdown-toggle"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
            id="viewswitch-charts-dropdown"
            :class="{
              'router-link-active': isChartRoute,
            }"
            >Charts</a
          >
          <span class="dropdown-menu charts">
            <router-link v-for="entry in chartEntries"
              :to="{ name: entry.route_name }"
              class="dropdown-item"
            >
              {{$t(entry.title)}}
            </router-link>
          </span>
        </li>

      </ul>
    </div>
  </div>
</template>

<script>
  const CHART_ENTRIES = [
    {
      title: "Web of Transnational Deals",
      route_name: "web-of-transnational-deals"
    }, {
      title: "Produce Info Map",
      route_name: "produce-info"
    }
  ]

  export default {
    name: "ViewSwitcher",
    data() {
      return {
        label: {
          deals: this.$t("Deals"),
          investors: this.$t("Investors"),
        },
        chartEntries: CHART_ENTRIES,
     };
    },
    computed: {
      isListRoute() {
        return ["list_deals", "list_investors"].includes(this.$route.name);
      },
      isChartRoute() {
        return this.chartEntries.map(e => e.route_name).includes(this.$route.name);
      },
      dataItemName() {
        if (this.$route.name === "list_deals") {
          return this.label.deals;
        } else if (this.$route.name === "list_investors") {
          return this.label.investors;
        } else {
          return this.$t("Data");
        }
      },
    },
  };
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
    z-index: 100;
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
            &.investors {
              background-color: $lm_investor;
            }
            &:hover {
              color: black;
            }
          }
          &:hover {
            color: $lm_orange;
          }
        }
        &.dropdown {
          &.show {
            .nav-link:not(.router-link-active) {
              color: $lm_orange;
            }
          }
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
                &.investors {
                  background-color: $lm_investor;
                }
                &:hover {
                  color: black;
                }
              }
              &:hover {
                color: $lm_orange;
              }
              &.investors:hover {
                color: $lm_investor;
              }
            }
            &.charts {
              width: auto;
              right: 0;
              left: auto;
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