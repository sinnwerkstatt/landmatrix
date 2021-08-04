<template>
  <div>
    <h3>{{ $t("Comments") }}</h3>
    <div id="comments">
      <ul>
        <li v-for="comm in comments" :key="comm.id">
          <dl class="comment">
            <dt>
              {{ dayjs(comm.submit_date).tz("UTC").format("YYYY-MM-DD HH:mm UTC") }}
              by {{ comm.userinfo.name }}
            </dt>
            <dd>
              <p>{{ comm.comment }}</p>
            </dd>
          </dl>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
  import dayjs from "dayjs";

  import utc from "dayjs/plugin/utc";
  import timezone from "dayjs/plugin/timezone";

  dayjs.extend(utc);
  dayjs.extend(timezone);

  export default {
    props: { comments: { type: Array, required: true } },
    methods: { dayjs },
  };
</script>

<style lang="scss" scoped>
  p {
    white-space: pre-line;
  }
  ul {
    list-style: none;
    padding: 0;
  }
  li {
    padding: 1.5rem 1rem;
    border-bottom: 1px solid var(--color-lm-light);
  }
  dt {
    font-weight: normal;
    font-size: 0.7125rem;
    padding-bottom: 0.5rem;
  }
</style>
