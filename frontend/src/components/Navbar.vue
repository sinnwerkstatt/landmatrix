<template>
  <nav class="navbar sticky-top navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">
        <img src="/static/img/lm-logo.png" alt="Landmatrix Logo" />
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#main-navbar-collapse"
        aria-controls="main-navbar-collapse"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="main-navbar-collapse">
        <ul class="navbar-nav">
          <li class="nav-item">
            <a class="nav-link" href="/global/">Global</a>
          </li>
          <li class="nav-item">
            <v-select
              class="nav-link"
              :options="regions"
              label="title"
              placeholder="Region"
            />
          </li>
          <li class="nav-item">
            <v-select
              class="nav-link"
              :options="countries"
              label="title"
              placeholder="Countries"
            />
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/stay-informed/" role="button">
              <span class="nav-text">Stay informed</span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/get-involved/" role="button">
              <span class="nav-text">Get involved</span>
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/faq/" role="button">
              <span class="nav-text">FAQ</span>
            </a>
          </li>
        </ul>
        <ul class="navbar-nav ml-auto">
          <li v-if="user.is_authenticated" class="nav-item">
            <p class="navbar-text dropdown-header">
              {{ user.full_name }}
              <br />
              <small>BOFH</small>
            </p>
          </li>
          <li v-if="user.is_authenticated" class="nav-item dropdown">
            <a
              href="#"
              role="button"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              id="navbarDropdown"
            >
              <i
                class="fa"
                :class="user.is_impersonate ? 'fa-user-secret' : 'fa-user'"
              ></i>
            </a>
            <div
              class="dropdown-menu dropdown-menu-right"
              aria-labelledby="#navbarDropdown"
            >
              <a
                v-if="user.is_impersonate"
                class="dropdown-item"
                href="/impersonate/stop/"
              >
                Stop impersonation</a
              >
              <hr v-if="user.is_impersonate" />
              <a class="dropdown-item" href="/editor/">Dashboard</a>
              <a class="dropdown-item" href="/manage/">Manage</a>
              <router-link class="dropdown-item" :to="{name:'deal_add'}">Add a deal</router-link>
              <a class="dropdown-item" href="/logout/">Logout</a>
            </div>
          </li>
          <li v-if="!user.is_authenticated" class="nav-item">
            <a
              href="/accounts/login/?next=/"
              role="button"
              title="Login/Register"
              class="nav-link"
            >
              <i class="fa fa-user"></i>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
  export default {
    // props: ['deal_id'],
    data() {
      return {
        regions: REGIONS,
        countries: COUNTRIES,
        user: DJANGO_USER,
      };
    },
  };
</script>

<style lang="scss" scoped>
  @import "../scss/colors";

  .bg-light {
    background-color: $lm_light !important;
  }

  .navbar-light .navbar-nav .nav-item .nav-link {
    font-size: 18px;
    color: $lm_dark;
    padding: 15px;

    &:hover {
      color: $primary;
    }
  }

  .navbar {
    border-bottom: 1px solid #bebebe;
    padding: 0;
  }

  .navbar-brand {
    width: 180px;
    height: 50px;
    display: block;
    padding: 5px;
    margin-left: 0 !important;
    margin-top: 8px;
    margin-right: 40px;
    margin-bottom: 15px;

    > img {
      width: 100%;
    }
  }
</style>

<style lang="scss">
  /* this needs to be here, in an unscoped style block */
  .vs--searchable {
    min-width: 80%;

    .vs__dropdown-toggle {
      border: none !important;
    }
  }
</style>
