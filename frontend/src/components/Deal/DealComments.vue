<template>
  <div>
    <h3>{{ $t("Comments") }}</h3>
    <div id="comments">
      <ul>
        <li v-for="comm in comments">
          <dl class="comment">
            <dt>
              <small>
                {{ dayjs(comm.submit_date).tz("UTC").format("MMM DD, YYYY HH:mm UTC") }}
                by {{ comm.userinfo.name }}
              </small>
            </dt>
            <dd>
              <p v-html="comm.comment" />
            </dd>
          </dl>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  import dayjs from "dayjs";
  dayjs.extend(require("dayjs/plugin/utc"));
  dayjs.extend(require("dayjs/plugin/timezone"));

  export default {
    props: ["comments"],
    methods: {
      dayjs,
    },
  };
</script>
