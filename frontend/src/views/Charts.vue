<template>
  <div class="">
    <nav class="navbar navbar-light bg-light">
      <div class="container-fluid">
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="/charts/web-of-transnational-deals/">
                Web of transnational deals
              </a>
            </li>
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                id="navbarDropdown"
                role="button"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
              >
                Dynamics Overview
              </a>
              <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                <a class="dropdown-item" href="/charts/intention/"
                  >Intention of investment</a
                >
                <a class="dropdown-item" href="/charts/negotiation-status/"
                  >Negotiation status</a
                >
                <a class="dropdown-item" href="/charts/implementation-status/"
                  >Implementation status</a
                >
                <a class="dropdown-item" href="/charts/intention-agriculture/"
                  >Investment in Agriculture</a
                >
                <div class="dropdown-divider"></div>
              </div>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/charts/map-of-investments/">
                Global map of investments
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/charts/perspective/">It's a big deal</a>
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
                <a class="dropdown-item" href="/charts/agricultural-drivers/"
                  >Agricultural Drivers</a
                >
                <a class="dropdown-item" href="/charts/produce-info/">Produce Info</a>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
  import store from "../store";

  export default {
    name: "Charts",
    beforeRouteEnter(to, from, next) {
      store.dispatch("setPageContext", {
        title: "Web of transnational deals",
        breadcrumbs: [{ href: "/charts/", name: "Data" }, { name: "Charts" }],
      });
      next();
    },
  };
</script>

<style scoped></style>
