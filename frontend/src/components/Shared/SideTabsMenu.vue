<template>
  <div class="side-tabs-menu" :class="{'expanded': expanded}">
    <div class="toggle">
      <a class="burger" @click.prevent="expanded=!expanded">
        <i class="fas fa-bars" :class="{'fa-bars': !expanded, 'fa-times': expanded}"></i>
      </a>
      <h3>{{ activeTabName }}</h3>
    </div>
    <ul class="lm-nav">
      <li
        v-for="(tabname, tabid) in tabs"
        :key="tabid"
        :class="{ active: active_tab === `#${tabid}` }"
        @click.prevent.stop="navigateTo(`#${tabid}`)"
      >
        <a :href="`#${tabid}`" @click.prevent.stop="navigateTo(`#${tabid}`)">
          {{ tabname }}
        </a>
      </li>
    </ul>
  </div>
</template>


<script>
  export default {
    name: "DealEdit",
    props: {
      tabs: [],
      active_tab: null
    },
    data() {
      return {
        expanded: false
      };
    },
    computed: {
      activeTabName() {
        let tabId = this.active_tab.substring(1);
        return this.tabs[tabId];
      }
    },
    methods: {
      navigateTo(hash) {
        this.expanded = false;
        this.$emit("updateRoute", hash);
      }
    }
  };
</script>


<style type="scss" scoped>
  .side-tabs-menu {
    grid-column: span 3;
    height: 100%;
    width: 100%;
    overflow-y: auto;
    padding: 0 1rem 0 0;


    /* IE and Edge */
    -ms-overflow-style: none;
    /* Firefox */
    scrollbar-width: none;

    position: relative;

  }

  .side-tabs-menu::-webkit-scrollbar {
    display: none;
  }

  .toggle {
    font-size: 2rem;
    display: none;
  }

  .burger {
    width: 1.7rem;
  }


  .toggle h3 {
    margin: 0;
    margin-left: 1rem;
  }


  @media only screen and (max-width: 992px) {
    .toggle {
      display: flex;
      align-items: center;
    }

    .lm-nav {
      display: none;
    }

    .side-tabs-menu.expanded .lm-nav {
      display: block;
    }

  }
</style>
