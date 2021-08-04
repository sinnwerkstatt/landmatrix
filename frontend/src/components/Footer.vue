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
  footer {
    background: var(--color-lm-dark);
    color: white;
    font-size: 0.875rem;
    font-weight: 400 !important;
    position: relative;

    .container {
      padding: 0.3125rem 1rem;
    }

    .social-buttons {
      .lm-footer {
        font-size: 1.25rem;
      }
      position: absolute;
      right: 1rem;
      bottom: 0;
      a {
        margin-left: 1em;
        &:hover {
          text-decoration: none;
          color: var(--color-lm-orange-light);
        }
      }
    }
  }
</style>
