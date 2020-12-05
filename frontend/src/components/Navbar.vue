<template>
  <nav class="navbar sticky-top navbar-expand-xl navbar-light bg-light">
    <div class="container-fluid">
      <router-link class="navbar-brand" :to="'/'">
        <img src="/static/images/lm-logo.png" alt="Landmatrix Logo" />
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
          <li class="nav-item dropdown">
            <a
              href="#"
              role="button"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              id="map-dropdown"
            >
              {{ $t("Data") }}
            </a>
            <div class="dropdown-menu">
              <router-link
                v-for="data_link in data_links"
                :to="data_link.link"
                class="dropdown-item"
              >
                {{ $t(data_link.name) }}
              </router-link>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a
              href="#"
              role="button"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              id="obs-dropdown"
            >
              {{ $t("Observatories") }}
            </a>
            <div class="dropdown-menu">
              <template v-for="(obs, obsgroup) in observatories_group">
                <!--                <div class="dropdown-divider"></div>-->
                <div class="dropdown-menu-group">
                  <router-link
                    v-for="observatory in obs"
                    class="dropdown-item"
                    :to="`/observatory/${observatory.meta.slug}/`"
                  >
                    {{ observatory.title }}
                  </router-link>
                </div>
              </template>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a
              href="#"
              role="button"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              id="res-dropdown"
            >
              {{ $t("Resources") }}
            </a>
            <div class="dropdown-menu">
              <router-link
                v-for="cat in blogcategories"
                class="dropdown-item"
                :to="`/stay-informed/?category=${cat.slug}`"
              >
                {{ cat.name }}
              </router-link>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a
              href="#"
              role="button"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
              id="about-dropdown"
            >
              {{ $t("About") }}
            </a>
            <div class="dropdown-menu">
              <router-link
                v-for="about_link in about_links"
                :to="about_link.link"
                class="dropdown-item"
              >
                {{ $t(about_link.name) }}
              </router-link>
            </div>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="`/faq/`">{{ $t("FAQ") }}</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="`/get-involved/`">{{
              $t("Contribute")
            }}</router-link>
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
              <small>{{ user.role }}</small>
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
              <a class="dropdown-item" href="/newdeal/case_statistics/">{{
                $t("Case statistics")
              }}</a>
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
  import gql from "graphql-tag";

  export default {
    components: { NavbarSelect },
    data() {
      return {
        username: null,
        password: null,
        login_failed_message: "",
        LANGUAGE: LANGUAGE,
        LANGUAGES: { en: "English", es: "Español", fr: "Français" },
        blogcategories: [],
        data_links: [
          { name: "Map", link: { name: "map" } },
          { name: "Deals", link: { name: "list_deals" } },
          { name: "Investors", link: { name: "list_investors" } },
          { name: "Charts", link: { name: "charts" } },
        ],
        about_links: [
          { name: "Land Matrix Initiative", link: "/the-land-matrix-initiative/" },
          { name: "Partners and donors", link: "/partners-and-donors/" },
          { name: "Privacy policy", link: "/privacy-policy/" },
          { name: "Disclaimer", link: "/disclaimer/" },
          { name: "Impressum", link: "/impressum-legal-notice/" },
        ],
      };
    },
    apollo: {
      blogcategories: gql`
        query {
          blogcategories {
            id
            name
            slug
          }
        }
      `,
    },
    computed: {
      user() {
        return this.$store.state.page.user;
      },
      observatories_group() {
        let ret = { global: [], regions: [], countries: [] };
        this.$store.state.page.observatories.forEach((ob) => {
          if (ob.country) ret.countries.push(ob);
          else if (ob.region) ret.regions.push(ob);
          else ret.global.push(ob);
        });
        return ret;
      },
    },
    methods: {
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
    background-color: white !important;
  }

  .navbar-light .navbar-nav .nav-item .nav-link {
    font-size: 16px;
    line-height: 18px;
    font-weight: 500;
    color: black;
    padding: 0.5rem 1.1rem;

    &:hover {
      color: $primary;
    }

    &.active {
      background: $primary;
    }
  }

  .navbar {
    border-bottom: 10px solid $lm_orange;
    padding: 0;
    .dropdown-menu {
      border: 1px solid $lm_orange;
      border-radius: 0;
      padding: 0;
      .dropdown-menu-group + .dropdown-menu-group {
        margin: 0.5rem 0;
        border-top: 1px solid #e9ecef;
      }
    }
  }
  .navbar-nav {
    .navbar-text {
      padding-top: 0.2rem;
      padding-bottom: 0.2rem;
    }
  }

  .navbar-brand {
    margin-top: 2px;
    margin-right: 1.5rem;
    margin-left: 0.7rem;
    > img {
      height: 38px;
      width: 144px;
      min-width: 144px;
      max-width: 144px;
    }
  }
</style>
