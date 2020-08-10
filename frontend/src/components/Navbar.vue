<template>
  <nav class="navbar sticky-top navbar-expand-xl navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">
        <img src="/static/images/lm-logo.png" alt="Landmatrix Logo" />
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
            <a class="nav-link" href="/global/">{{ $t("Global") }}</a>
          </li>
          <navbar-select
            :title="$t('Regions')"
            :options="regions"
            @select="openLink('region', $event)"
          ></navbar-select>
          <navbar-select
            :title="$t('Countries')"
            :options="countries"
            @select="openLink('country', $event)"
          ></navbar-select>
          <li class="nav-item">
            <a class="nav-link" href="/stay-informed/">{{ $t("Stay informed") }}</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/get-involved/">{{ $t("Get involved") }}</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="/faq/">{{ $t("FAQ") }}</a>
          </li>
        </ul>
        <ul class="navbar-nav ml-auto">
          <li class="nav-item dropdown">
            <a
              href="#"
              role="button"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              id="languageDropdown"
            >
              <i class="fa fa-language" aria-hidden="true" style="display: inline;"></i>
              {{ LANGUAGES[LANGUAGE] }}
            </a>
            <div class="dropdown-menu">
              <a
                v-for="(lingo, lcode) in LANGUAGES"
                :href="`/language/${lcode}/`"
                class="dropdown-item"
                :class="{ active: lcode === LANGUAGE }"
              >
                {{ lingo }} ({{ lcode }})
              </a>
            </div>
          </li>
          <li v-if="user" class="nav-item">
            <p class="navbar-text dropdown-header">
              {{ user.full_name }}
              <br />
              <small>{{ user_role }}</small>
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
              ref="userMenu"
            >
              <!--suppress HtmlUnknownTarget -->
              <a
                v-if="user.is_impersonate"
                class="dropdown-item"
                href="/impersonate/stop/?next=/dashboard/"
              >
                {{ $t("Stop impersonation") }}
              </a>
              <div v-if="user.is_impersonate" class="dropdown-divider"></div>
              <a class="dropdown-item" href="/editor/">{{ $t("Dashboard") }}</a>
              <a class="dropdown-item" href="/manage/">{{ $t("Manage") }}</a>
              <a class="dropdown-item" href="/deal/add/">{{ $t("Add a deal") }}</a>
              <a class="dropdown-item" @click.prevent="dispatchLogout">{{
                $t("Logout")
              }}</a>
            </div>
          </li>
          <li v-if="!user" class="nav-item dropdown">
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
              <form class="px-4 pt-3">
                <div class="form-group">
                  <input
                    v-model="username"
                    type="text"
                    class="form-control"
                    id="username"
                    autocomplete="username"
                    placeholder="username"
                  />
                </div>
                <div class="form-group">
                  <input
                    v-model="password"
                    type="password"
                    class="form-control"
                    id="password"
                    autocomplete="current-password"
                    placeholder="password"
                  />
                </div>
                <button
                  type="submit"
                  @click.prevent="dispatchLogin"
                  class="btn btn-secondary"
                >
                  {{ $t("Login") }}
                </button>
                <p class="mt-3 text-danger small">{{ login_failed_message }}</p>
              </form>
              <div class="dropdown-divider"></div>
              <a class="dropdown-item" href="/accounts/register/">{{
                $t("New around here? Sign up")
              }}</a>
              <a class="dropdown-item" href="/accounts/password_reset/">{{
                $t("Forgot password?")
              }}</a>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
  import NavbarSelect from "/components/NavbarSelect";

  export default {
    components: { NavbarSelect },
    data() {
      return {
        username: null,
        password: null,
        login_failed_message: "",
        LANGUAGE: LANGUAGE,
        LANGUAGES: { en: "English", es: "Español", fr: "Français" },
      };
    },
    computed: {
      user() {
        return this.$store.state.page.user;
      },
      regions() {
        return this.$store.state.page.regions;
      },
      countries() {
        return this.$store.state.page.countries;
      },
      user_role() {
        if (this.user && this.user.groups.length) {
          let groupi = this.user.groups
            .map((g) => g.name)
            .filter((name) => {
              return ["Administrators", "Editors", "Reporters"].indexOf(name) > -1;
            });

          if (groupi.length) {
            let ret = "";
            if (groupi.indexOf("Reporters") > -1) ret = "Reporter";
            if (groupi.indexOf("Editors") > -1) ret = "Editor";
            if (groupi.indexOf("Administrators") > -1) ret = "Administrator";
            let uri = this.user.userregionalinfo;
            if (uri) {
              let area = uri.region.map((c) => c.name);
              area = area.concat(uri.country.map((c) => c.name));
              if (area.length) {
                return `${ret} of ${area.join(", ")}`;
              }
            }
            return ret;
          }
        }
        return "No Role";
      },
    },
    methods: {
      openLink(target_url, option) {
        this.$router.push(`/${target_url}/${option.slug}/`);
      },
      dispatchLogout() {
        this.$store.dispatch("logout");
      },
      dispatchLogin() {
        this.$store
          .dispatch("login", { username: this.username, password: this.password })
          .then(() => {
            this.login_failed_message = "";
            if (this.$refs.userMenu) {
              this.$refs.userMenu.classList.remove("show");
            }
          })
          .catch((response) => {
            this.login_failed_message = response.error;
          });
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

    &.active {
      background: $primary;
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
