<template>
  <div>
    <h3>{{ $t("Comments") }}</h3>
    <div id="comments">
      <ul>
        <li v-for="comm in cmmnts" :key="comm.id">
          <dl class="comment">
            <dt>
              {{ dayjs(comm.submit_date).tz("UTC").format("YYYY-MM-DD HH:mm UTC") }}
              by {{ comm.userinfo.name }}
            </dt>
            <dd>
              <strong>{{ comm.title }}</strong>
              <p>{{ comm.comment }}</p>
              <div class="">
                <!--                <button @click.prevent="editComment(comm.id)">Edit</button>-->
                <!--                |-->
                <button class="delete-button" @click.prevent="removeComment(comm.id)">
                  Delete
                </button>
              </div>
            </dd>
          </dl>
        </li>
      </ul>
    </div>
    <form class="mt-5" @submit.prevent="sendComment">
      <h4>{{ $t("Add a comment") }}</h4>

      <div v-if="$store.getters.userAuthenticated">
        Name: <strong>{{ $store.state.page.user.full_name }}</strong>
      </div>
      <div v-else class="add-a-comment-header">
        <input v-model="name" :placeholder="$t('Name')" required />
        <input v-model="email" :placeholder="$t('Email')" required type="email" />
      </div>

      <input v-model="title" :placeholder="$t('Comment title')" />
      <textarea
        v-model="comment"
        :placeholder="$t('Comment')"
        cols="50"
        required
        rows="3"
      />

      <label>
        <input required style="width: inherit" type="checkbox" />
        {{ $t("I've read and agree to the") }}
        <a href="/about/data-policy/" target="_blank">{{ $t("Data policy") }}</a
        >.
      </label>
      <vue-hcaptcha
        ref="hcaptcha"
        :re-captcha-compat="false"
        :sitekey="VITE_HCAPTCHA_SITEKEY"
        @verify="captchaVerified"
      />
      <div>
        <button :disabled="submit_disabled" class="btn btn-primary" type="submit">
          {{ $t("Submit") }}
        </button>
      </div>
    </form>
  </div>
</template>

<script lang="ts">
  import { apolloClient } from "$utils/apolloclient";
  import VueHcaptcha from "@hcaptcha/vue-hcaptcha";
  import dayjs from "dayjs";
  import timezone from "dayjs/plugin/timezone";

  import utc from "dayjs/plugin/utc";
  import gql from "graphql-tag";
  import Vue from "vue";
  dayjs.extend(utc);
  dayjs.extend(timezone);

  export default Vue.extend({
    components: { VueHcaptcha },
    props: {
      comments: { type: Array, required: true },
      dealId: { type: [Number, String], required: true },
    },
    data() {
      return {
        cmmnts: this.comments,
        name: "",
        email: "",
        title: "",
        comment: "",
        token: "",
        submit_disabled: true,
        VITE_HCAPTCHA_SITEKEY:
          import.meta.env.VITE_HCAPTCHA_SITEKEY ||
          "10000000-ffff-ffff-ffff-000000000001",
      };
    },
    methods: {
      dayjs,
      captchaVerified(token) {
        this.token = token;
        this.submit_disabled = false;
      },
      sendComment() {
        apolloClient
          .mutate({
            mutation: gql`
              mutation AddComment(
                $id: Int!
                $title: String
                $comment: String!
                $token: String!
                $name: String
                $email: String
              ) {
                add_public_deal_comment(
                  id: $id
                  title: $title
                  comment: $comment
                  token: $token
                  name: $name
                  email: $email
                )
              }
            `,
            variables: {
              id: +this.dealId,
              title: this.title,
              comment: this.comment,
              token: this.token,
              name: this.name,
              email: this.email,
            },
          })
          .then(({ data: { add_public_deal_comment } }) => {
            if (add_public_deal_comment) {
              let newD = {
                id: Math.floor(Math.random() * 100000000),
                submit_date: new Date(),
                userinfo: { name: this.name || this.$store.state.page.user.full_name },
                comment: this.comment,
                title: this.title,
              };
              this.cmmnts.push(newD);
              this.title = "";
              this.comment = "";
              this.$refs.hcaptcha.reset();
            } else {
              console.error("problem");
            }
          });
      },
      removeComment(id) {
        apolloClient
          .mutate({
            mutation: gql`
              mutation ($id: Int!) {
                remove_public_deal_comment(id: $id)
              }
            `,
            variables: { id },
          })
          .then(({ data: { remove_public_deal_comment } }) => {
            if (remove_public_deal_comment) {
              const idx = this.cmmnts.findIndex((c) => c.id === id);
              this.cmmnts.splice(idx, 1);
            }
            console.log({ remove_public_deal_comment });
          });
      },
      editComment(id) {
        // apolloClient.mutate({
        //   mutation: gql`
        //     mutation ($id: Int!) {
        //       edit_public_deal_comment(id: $id)
        //     }
        //   `,
        //   variables: { id },
        // });
      },
    },
  });
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
    border-bottom: 1px solid var(--color-lm-dark);
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
  .delete-button {
    font-size: 0.75rem;
    color: red;
    border: 0;
    background: inherit;
  }
</style>
