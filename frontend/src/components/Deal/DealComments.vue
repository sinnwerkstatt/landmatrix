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
    <form>
      <h4>{{ $t("Add a comment") }}</h4>
      <div class="add-a-comment-header">
        <input :placeholder="$t('Name')" required />
        <input :placeholder="$t('Email')" type="email" required />
      </div>
      <input :placeholder="$t('Comment title')" />
      <textarea cols="50" rows="3" :placeholder="$t('Comment')" required></textarea>
      <label>
        <input required type="checkbox" style="width: inherit" />
        {{ $t("I've read and agree to the") }}
        <a href="/about/data-policy/" target="_blank">{{ $t("Data policy") }}</a
        >.
      </label>
      <vue-hcaptcha
        sitekey="ee77472a-0484-49a2-9e80-bcb765c774b1"
        re-captcha-compat="false"
        @verify="captchaVerified"
      />
      <div>
        <button disabled type="submit" class="btn btn-primary">
          {{ $t("Submit") }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
  import dayjs from "dayjs";

  import utc from "dayjs/plugin/utc";
  import timezone from "dayjs/plugin/timezone";
  import VueHcaptcha from "@hcaptcha/vue-hcaptcha";

  dayjs.extend(utc);
  dayjs.extend(timezone);

  export default {
    components: { VueHcaptcha },
    props: { comments: { type: Array, required: true } },
    methods: {
      dayjs,
      captchaVerified(token, eKey) {
        console.log({ token, eKey });
      },
    },
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
  h4 {
    font-size: 1.125rem;
  }
  .add-a-comment-header {
    display: flex;
    width: 100%;
    flex-flow: column;
    gap: 1em;

    @media screen and (min-width: 800px) {
      flex-flow: row nowrap;
    }
  }
  input,
  textarea {
    width: 100%;
    margin: 0.5em 0;
    //&[required] {
    //  font-weight: bold;
    //  color: red;
    //  display: inline;
    //}
  }
</style>
