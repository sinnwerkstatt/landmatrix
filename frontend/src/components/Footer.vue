<template>
  <footer>
    <div class="container">
      <div id="footer-etc" class="row">
        <div class="col-12 text-center">
          <p class="mb-0">
            <a :href="legacy_link">&copy; {{ currentyear }}</a>
            The Land Matrix | {{ $t("All rights reserved") }}
          </p>
        </div>
        <div class="social-buttons">
          <a target="_blank" href="https://twitter.com/Land_Matrix">
            <i class="lm-footer lm-twitter-square"></i>
          </a>
          <a target="_blank" href="https://www.facebook.com/LandMatrix">
            <i class="lm-footer lm-facebook-square"></i>
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
  export default {
    name: "Footer",
    data() {
      return {
        currentyear: new Date().getFullYear(),
      };
    },
    computed: {
      legacy_link() {
        let base = "/legacy";
        return base + this.$route.path;
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../scss/colors";

  footer {
    background: $lm_dark;
    padding: 0 10px;
    font-size: 14px;
    color: white;
    font-weight: 400 !important;
    margin-top: 0;
    position: relative;

    .container {
      padding-top: 5px;
      padding-bottom: 5px;
    }
    hr {
      border-top: 1px solid #9b9b9b;
    }

    .lm-footer {
      font-size: 20px;
    }
    .social-buttons {
      position: absolute;
      right: 15px;
      bottom: 1px;
      a {
        margin-left: 1em;
        &:hover {
          text-decoration: none;
          color: theme-color-level("primary", -3);
        }
      }
    }
  }
</style>
