<template>
  <nav class="navbar sticky-top navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">
        <img src="../images/lm-logo.png" alt="Landmatrix Logo" />
      </router-link>
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
            <router-link class="nav-link" to="/global/">Global</router-link>
          </li>
          <li class="nav-item">
            <multiselect
              class="nav-link"
              :options="regions"
              label="title"
              placeholder="Region"
            />
          </li>
          <li class="nav-item">
            <multiselect
              class="nav-link"
              :options="countries"
              label="title"
              placeholder="Countries"
            />
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/stay-informed/" role="button">
              <span class="nav-text">Stay informed</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/get-involved/" role="button">
              <span class="nav-text">Get involved</span>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/faq/" role="button">
              <span class="nav-text">FAQ</span>
            </router-link>
          </li>
        </ul>
        <ul class="navbar-nav ml-auto">
          <li v-if="user" class="nav-item">
            <p class="navbar-text dropdown-header">
              {{ user.full_name }}
              <br />
              <small>BOFH</small>
            </p>
          </li>
          <li v-if="user" class="nav-item dropdown">
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
                href="/impersonate/stop/?next=/newdeal/dashboard/"
              >
                Stop impersonation</a
              >
              <div v-if="user.is_impersonate" class="dropdown-divider"></div>
              <router-link class="dropdown-item" :to="{name:'dashboard'}">Dashboard</router-link>
              <a class="dropdown-item" href="/manage/">Manage</a>
              <router-link class="dropdown-item" :to="{ name: 'deal_add' }"
                >Add a deal
              </router-link>
              <a class="dropdown-item" @click.prevent="dispatchLogout">Logout</a>
            </div>
          </li>
          <li v-else class="nav-item dropdown">
            <a
              href="#"
              role="button"
              title="Login/Register"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              id="navbarDropdownAnonymous"
            >
              <i class="fa fa-user"></i>
            </a>
            <div
              class="dropdown-menu dropdown-menu-right"
              aria-labelledby="#navbarDropdownAnonymous"
            >
              <form class="px-4 py-3">
                <div class="form-group">
                  <input
                    v-model="login_username"
                    type="text"
                    class="form-control"
                    id="username"
                    placeholder="username"
                  />
                </div>
                <div class="form-group">
                  <input
                    v-model="login_password"
                    type="password"
                    class="form-control"
                    id="password"
                    placeholder="password"
                  />
                </div>
                <button
                  type="submit"
                  @click.prevent="dispatchLogin"
                  class="btn btn-secondary"
                >
                  Login
                </button>
              </form>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" href="/accounts/register/">New around here? Sign up</a>
              <a class="dropdown-item" href="/accounts/password_reset/">Forgot password?</a>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
  export default {
    data() {
      return {
        regions: REGIONS,
        countries: COUNTRIES,
        login_username: null,
        login_password: null,
        login_remember: false,
      };
    },
    computed: {
      user() {
        return this.$store.state.user;
      },
    },
    methods: {
      dispatchLogout() {
        this.$store.dispatch("logout");
      },
      dispatchLogin() {
        this.$store.dispatch("login", {
          username: this.login_username,
          password: this.login_password,
        });
        // TODO: handle error here.
      },
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