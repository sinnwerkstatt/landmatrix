<template>
  <div class="map-data-charts row">
    <div class="map col-4">
      <router-link :to="{name: 'map'}" class="square">
        <div>
          <h3 class="title">Map</h3>
          <div class="icon">
            <svg width="72" height="96" viewBox="0 0 72 96" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M32.3003 94.0631C5.05688 54.5683 0 50.5149 0 36C0 16.1177 16.1177 0 36 0C55.8823 0 72 16.1177 72 36C72 50.5149 66.9431 54.5683 39.6997 94.0631C37.9119 96.6458 34.0879 96.6456 32.3003 94.0631ZM36 51C44.2843 51 51 44.2843 51 36C51 27.7157 44.2843 21 36 21C27.7157 21 21 27.7157 21 36C21 44.2843 27.7157 51 36 51Z" fill="#F78F1F"/>
            </svg>
          </div>
          <div class="text">Explore the map for information about land deals from global down to regional and country level.</div>
        </div>
      </router-link>
    </div>
    <div class="data col-4">
      <router-link :to="{name: 'list_deals'}" class="square">
        <div>
          <h3 class="title">Data</h3>
          <div class="icon">
            <svg width="96" height="84" viewBox="0 0 96 84" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M87 0H9C4.02938 0 0 4.02938 0 9V75C0 79.9706 4.02938 84 9 84H87C91.9706 84 96 79.9706 96 75V9C96 4.02938 91.9706 0 87 0ZM42 72H12V54H42V72ZM42 42H12V24H42V42ZM84 72H54V54H84V72ZM84 42H54V24H84V42Z" fill="#F78F1F"/>
            </svg>
          </div>
          <div class="text">Search and filter the dataset through pre-configured entry points or drill down to single deals.</div>
        </div>
      </router-link>
    </div>
    <div class="charts col-4">
      <router-link :to="{name: 'charts'}" class="square">
        <div>
          <h3 class="title">Charts</h3>
          <div class="icon">
            <svg width="96" height="72" viewBox="0 0 96 72" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M62.4 48H69.6C70.8 48 72 46.8 72 45.6V20.4C72 19.2 70.8 18 69.6 18H62.4C61.2 18 60 19.2 60 20.4V45.6C60 46.8 61.2 48 62.4 48ZM80.4 48H87.6C88.8 48 90 46.8 90 45.6V2.4C90 1.2 88.8 0 87.6 0H80.4C79.2 0 78 1.2 78 2.4V45.6C78 46.8 79.2 48 80.4 48ZM26.4 48H33.6C34.8 48 36 46.8 36 45.6V32.4C36 31.2 34.8 30 33.6 30H26.4C25.2 30 24 31.2 24 32.4V45.6C24 46.8 25.2 48 26.4 48ZM44.4 48H51.6C52.8 48 54 46.8 54 45.6V8.4C54 7.2 52.8 6 51.6 6H44.4C43.2 6 42 7.2 42 8.4V45.6C42 46.8 43.2 48 44.4 48ZM93 60H12V3C12 1.3425 10.6575 0 9 0H3C1.3425 0 0 1.3425 0 3V66C0 69.3131 2.68687 72 6 72H93C94.6575 72 96 70.6575 96 69V63C96 61.3425 94.6575 60 93 60Z" fill="#F78F1F"/>
            </svg>
          </div>
          <div class="text">Generate your own infographics using a wide selection of charts to illustrate information about deals.</div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
  export default {
  };
</script>

<style lang="scss" scoped>
.map-data-charts {
  margin-top: 2em;
  margin-bottom: 2em;
  .square {
    display: block;
    background-color: #F9F9F9;
    text-align: center;
    border-radius: 5px;
    padding: 15px;
    color: black;

    &:hover {
      filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.35));
      text-decoration: none;
    }

    .title {
    }
    .icon {
      margin-top: 1em;
      height: 96px;
    }
    .text {
      margin-top: 0.5em;
      font-size: 18px;
    }
  }
}
</style>
