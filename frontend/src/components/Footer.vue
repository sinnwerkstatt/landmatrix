<template>
  <footer>
    <div class="container">
      <div id="footer-nav" class="row">
        <div
          class="col-md-3"
          v-for="footerCol in footerColumns"
          v-html="footerCol"
        ></div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <hr />
        </div>
      </div>
      <div id="footer-etc" class="row">
        <div class="col-md-6">
          <p>&copy; {{ currentyear }} The Land Matrix | All rights reserved</p>
        </div>
        <div class="col-md-6 text-right">
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
        currentyear: "2020",
        footerColumns: FOOTER_COLUMNS,
      };
    },
  };
</script>

<style lang="scss">
  @import "../scss/colors";

  footer {
    background: $lm_grey;
    padding: 10px;
    font-size: 16px;
    font-family: "Open Sans", sans-serif;
    color: $lm_dark;
    font-weight: 400 !important;
    hr {
      border-top: 1px solid #9b9b9b;
    }

    .lm-footer {
      font-size: 20px;
    }
  }
</style>
