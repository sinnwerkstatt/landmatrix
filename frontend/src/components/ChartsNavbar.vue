<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <button
        class="navbar-toggler ml-auto"
        type="button"
        data-toggle="collapse"
        data-target="#chartsNavbar"
        aria-controls="chartsNavbar"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="chartsNavbar">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'web-of-transnational-deals' }">
              Web of transnational deals
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'dynamics-overview' }">
              Dynamics Overview
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'global-map-of-investments' }">
              Global map of investments
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="{ name: 'its-a-big-deal' }">
              It's a big deal
            </router-link>
          </li>
          <li class="nav-item dropdown">
            <a
              class="nav-link dropdown-toggle"
              href="#"
              id="navbarDropdown2"
              role="button"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              Special Interest
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown2">
              <a class="dropdown-item" href="/charts/agricultural-drivers/">
                Agricultural Drivers
              </a>
              <a class="dropdown-item" href="/charts/produce-info/">Produce Info</a>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style lang="scss" scoped>
  @import "../scss/colors";

  nav {
    background-color: $lm_light !important;
    border: 1px solid $lm_light_border;
    padding: 0;
    a {
      padding: 10px 0;
    }
  }
  .router-link-exact-active {
    color: black;
    background: white;
  }
</style>
