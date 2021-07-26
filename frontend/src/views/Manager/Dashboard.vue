<template>
  <div class="container">
    <div class="row">
      <div class="col-md-6">
        Hier kann man Regionen und Laender auswaehlen... scheinbar zum filtern, glaub
        ich?
      </div>
      <div class="col-md-6">
        <form class="form-inline justify-content-between">
          <label>Impersonate</label>
          <multiselect
            v-model="userToImpersonate"
            :options="users"
            :custom-label="(u) => `${u.full_name} (${u.username})`"
          ></multiselect>
          <a
            v-if="userToImpersonate"
            type="submit"
            class="btn btn-primary"
            :href="`/impersonate/${userToImpersonate.id}/?next=/`"
          >
            Impersonate
          </a>
        </form>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6">
        <div class="well">
          <h3>
            Latest added
            <a class="" href="/editor/log/latest_added/?"><small>Show all</small></a>
          </h3>

          <table class="table table-condensed">
            <thead>
              <tr>
                <th class="deal">ID</th>
                <th class="user">Added by</th>
                <th class="comment">Comment</th>
                <th class="date">Added</th>
              </tr>
            </thead>
            <tbody></tbody>
          </table>
        </div>
      </div>
      <div class="col-md-6">
        <div class="well">
          <h3>
            Needs your attention
            <a class="" href="/editor/manage/"><small>Show all</small></a>
          </h3>

          <table class="table table-condensed">
            <thead>
              <tr>
                <th class="deal">ID</th>
                <th class="user">Last revision</th>
                <th class="state">State</th>
                <th class="state">Timestamp</th>
                <th class="action">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr class="update">
                <td class="deal">
                  <a href="/deal/6993/" class="label label-deal">6993</a>
                </td>

                <td class="user">andreas.nuesslein (No role)</td>
                <td class="state">Update</td>
                <td class="state">1&nbsp;week ago</td>
                <td class="action">
                  <a href="/deal/edit/6993/" class="approve label label-deal">
                    <i class="lm lm-thumbs-up"></i>Approve
                  </a>
                  <a href="/deal/edit/6993/" class="reject label label-deal">
                    <i class="lm lm-thumbs-down"></i>Reject
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="well">
          <h3>
            Feedback requests
            <a class="" href="/editor/manage/"><small>Show all</small></a>
          </h3>

          <p>No feedback requests lately.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import store from "$store";
  import gql from "graphql-tag";

  export default {
    beforeRouteEnter(to, from, next) {
      let title = "Dashboard";
      store.dispatch("setPageContext", {
        title: title,
        breadcrumbs: [{ link: { name: "wagtail" }, name: "Home" }, { name: title }],
      });
      next();
    },
    metaInfo() {
      return { title: this.$t("Dashboard") };
    },
    data: function () {
      return {
        users: [],
        userToImpersonate: null,
      };
    },
    apollo: {
      users: gql`
        {
          users {
            id
            full_name
            username
          }
        }
      `,
    },
  };
</script>

<style scoped>
  .multiselect {
    display: inline-block;
    width: 50%;
  }
</style>
