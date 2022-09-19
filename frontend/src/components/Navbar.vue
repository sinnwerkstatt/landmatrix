<template>
  <nav class="navbar navbar-expand-xl navbar-light">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">
        <img :src="lm_logo" alt="Land Matrix" />
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
      <div id="main-navbar-collapse" ref="mainbar" class="collapse navbar-collapse">
        <ul class="navbar-nav align-items-center">
          <li class="nav-item dropdown">
            <a
              id="map-dropdown"
              href="#"
              role="button"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              {{ $t("Data") }}
            </a>
            <div class="dropdown-menu">
              <router-link
                v-for="data_link in data_links"
                :key="data_link.name"
                :to="data_link.link"
                class="dropdown-item"
                @click.native="closeMenu"
              >
                {{ $t(data_link.name) }}
              </router-link>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a
              id="obs-dropdown"
              href="#"
              role="button"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              {{ $t("Observatories") }}
            </a>
            <div class="dropdown-menu">
              <div
                v-for="(obs, obsgroup) in observatories_group"
                :key="obsgroup"
                class="dropdown-menu-group"
              >
                <router-link
                  v-for="observatory in obs"
                  :key="observatory.id"
                  class="dropdown-item"
                  :to="`/observatory/${observatory.meta.slug}/`"
                  @click.native="closeMenu"
                >
                  {{ observatory.title }}
                </router-link>
              </div>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a
              id="res-dropdown"
              href="#"
              role="button"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              {{ $t("Resources") }}
            </a>
            <div class="dropdown-menu">
              <router-link
                v-for="cat in blogcategories"
                :key="cat.slug"
                class="dropdown-item"
                :to="`/resources/?category=${cat.slug}`"
                @click.native="closeMenu"
              >
                {{ $t(cat.name) }}
              </router-link>
            </div>
          </li>
          <li class="nav-item dropdown">
            <a
              id="about-dropdown"
              href="#"
              role="button"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              {{ $t("About") }}
            </a>
            <div class="dropdown-menu">
              <router-link
                v-for="about_link in aboutLinks"
                :key="about_link.link"
                :to="about_link.link"
                class="dropdown-item"
                @click.native="closeMenu"
              >
                {{ $t(about_link.name) }}
              </router-link>
            </div>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" :to="`/faq/`" @click.native="closeMenu">
              {{ $t("FAQ") }}
            </router-link>
          </li>
          <li class="nav-item">
            <router-link
              class="nav-link"
              :to="`/contribute/`"
              @click.native="closeMenu"
            >
              {{ $t("Contribute") }}
            </router-link>
          </li>
        </ul>
        <ul class="navbar-nav align-items-center ml-auto">
          <NavbarSearch />
          <li class="nav-item dropdown">
            <a
              id="languageDropdown"
              role="button"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              <i class="fa fa-language" aria-hidden="true"></i>
              {{ languages[language] }}
            </a>
            <div class="dropdown-menu">
              <div
                v-for="(lingo, lcode) in languages"
                :key="lingo"
                :class="{ active: lcode === language }"
                class="dropdown-item"
                @click="switchLanguage(lcode)"
              >
                {{ lingo }} ({{ lcode }})
              </div>
            </div>
          </li>
          <li v-if="user" class="nav-item dropdown">
            <a
              id="navbarDropdown"
              href="#"
              role="button"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              {{ user.username }}
              <i v-if="user.role === 3" class="fas fa-user-astronaut"></i>
              <i v-else-if="user.role === 2" class="fas fa-user-nurse"></i>
              <i v-else-if="user.is_impersonate" class="fa fa-user-secret"></i>
              <i v-else class="fa fa-user"></i>
            </a>
            <div
              ref="userMenu"
              class="dropdown-menu dropdown-menu-right"
              aria-labelledby="#navbarDropdown"
            >
              <p class="name-emblem">
                {{ user.full_name }}
                <br />
                <small>{{ user.role }}</small>
              </p>
              <div class="dropdown-divider"></div>
              <!--suppress HtmlUnknownTarget -->
              <a
                v-if="user.is_impersonate"
                class="dropdown-item"
                href="/impersonate/stop/?next=/dashboard/"
              >
                {{ $t("Stop impersonation") }}
              </a>
              <div v-if="user.is_impersonate" class="dropdown-divider"></div>

              <router-link class="dropdown-item" :to="{ name: 'manager' }">
                {{ $t("Manage") }}
              </router-link>
              <router-link class="dropdown-item" :to="{ name: 'case_statistics' }">
                {{ $t("Case statistics") }}
              </router-link>
              <div class="dropdown-divider"></div>
              <router-link class="dropdown-item" :to="{ name: 'deal_add' }">
                {{ $t("Add a deal") }}
              </router-link>

              <a class="dropdown-item" @click.prevent="dispatchLogout">
                {{ $t("Logout") }}
              </a>
            </div>
          </li>
          <li v-if="!user" class="nav-item dropdown">
            <a
              id="navbarDropdownAnonymous"
              href="#"
              role="button"
              title="Login/Register"
              class="nav-link dropdown-toggle"
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              <i class="far fa-user"></i>
            </a>
            <div
              class="dropdown-menu dropdown-menu-right"
              aria-labelledby="#navbarDropdownAnonymous"
            >
              <form class="px-4 pt-3" @submit.prevent="dispatchLogin">
                <div class="form-group">
                  <input
                    id="username"
                    v-model="username"
                    type="text"
                    class="form-control"
                    autocomplete="username"
                    placeholder="Username"
                  />
                </div>
                <div class="form-group">
                  <input
                    id="password"
                    v-model="password"
                    type="password"
                    class="form-control"
                    autocomplete="current-password"
                    placeholder="Password"
                  />
                </div>
                <button type="submit" class="btn btn-secondary">
                  {{ $t("Login") }}
                </button>
                <p class="text-danger small mt-3">{{ login_failed_message }}</p>
              </form>
              <div class="dropdown-divider"></div>
              <router-link :to="{ name: 'register' }" class="dropdown-item">
                {{ $t("New around here? Sign up") }}
              </router-link>
              <router-link :to="{ name: 'password_reset' }" class="dropdown-item">
                {{ $t("Forgot password?") }}
              </router-link>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script lang="ts">
  import NavbarSearch from "$components/NavbarSearch.vue";
  import lm_logo from "$static/images/lm-logo.png";
  import { blogcategories_query } from "$store/queries";
  import Cookies from "js-cookie";
  import Vue from "vue";

  export default Vue.extend({
    components: { NavbarSearch },
    data() {
      return {
        lm_logo,
        username: null,
        password: null,
        login_failed_message: "",
        language: Cookies.get("django_language") ?? "en",
        languages: { en: "English", es: "Español", fr: "Français", ru: "Русский" },
        blogcategories: [],
        data_links: [
          { name: "Map", link: { name: "map" } },
          { name: "Deals", link: { name: "list_deals" } },
          { name: "Investors", link: { name: "list_investors" } },
          { name: "Charts", link: { name: "charts" } },
        ],
      };
    },
    apollo: { blogcategories: blogcategories_query },
    computed: {
      user() {
        return this.$store.state.user;
      },
      aboutPages() {
        return this.$store.state.aboutPages;
      },
      aboutLinks() {
        return this.$store.state.aboutPages.map((page) => {
          return {
            name: page.title,
            link: `/about/${page.meta.slug}/`,
          };
        });
      },
      observatories_group() {
        let ret = { global: [], regions: [], countries: [] };
        this.$store.state.observatories.forEach((ob) => {
          if (ob.country) ret.countries.push(ob);
          else if (ob.region) ret.regions.push(ob);
          else ret.global.push(ob);
        });
        return ret;
      },
    },
    methods: {
      switchLanguage(locale) {
        this.$store.dispatch("setLocale", locale);
        this.$i18n.locale = locale;
        this.language = locale;
      },
      dispatchLogout() {
        this.$store.dispatch("logout").then(() => location.reload());
      },
      dispatchLogin() {
        this.$store
          .dispatch("login", { username: this.username, password: this.password })
          .then(() => {
            location.reload();
            // this.login_failed_message = "";
            // if (this.$refs.userMenu) {
            //   this.$refs.userMenu.classList.remove("show");
            // }
          })
          .catch((response) => {
            this.login_failed_message = response.error;
          });
      },
      closeMenu() {
        if (this.$refs.mainbar.classList.contains("show")) {
          this.$refs.mainbar.classList.remove("show");
        }
      },
    },
  });
</script>

<style lang="scss" scoped>
  nav {
    position: sticky;
    top: 0;
    z-index: 1030;
    background-color: white !important;
  }

  .navbar-light .navbar-nav .nav-item .nav-link {
    font-size: 16px;
    line-height: 18px;
    font-weight: 500;
    color: black;
    padding: 0.5rem 1.1rem;

    &:hover {
      color: var(--color-lm-orange);
    }

    &.active {
      background: var(--color-lm-orange);
    }
  }

  .navbar {
    border-bottom: 10px solid var(--color-lm-orange);
    padding: 0;

    .dropdown-menu {
      border: 1px solid var(--color-lm-orange);
      border-radius: 0;
      padding: 0;

      .dropdown-menu-group + .dropdown-menu-group {
        margin: 0;
        border-top: 1px solid #e9ecef;
      }

      .dropdown-item {
        padding: 0.5rem 1rem;
      }
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
  .name-emblem {
    padding: 0.5rem 0 0 1rem;
    line-height: 1.2em;
    color: gray;
  }

  .router-link-exact-active {
    pointer-events: none;
    &:hover {
      background: inherit;
      cursor: default;
    }
  }
</style>
