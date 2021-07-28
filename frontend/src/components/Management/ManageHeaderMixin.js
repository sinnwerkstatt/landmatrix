import { is_authorized } from "$utils/user";
import gql from "graphql-tag";

const ManageHeaderMixin = {
  props: {
    object: { type: Object, required: true },
    objectVersion: { type: [Number, String], default: null },
    otype: { type: String, default: "deal" },
  },
  data() {
    return {
      users: [],
      show_to_draft_overlay: false,
      show_to_delete_overlay: false,
      is_authorized,
      submit_for_review_link_title:
        this.otype === "deal"
          ? this.$t("Submits the deal for review")
          : this.$t("Submits the investor for review"),
      request_improvement_link_title:
        this.otype === "deal"
          ? this.$t(
              "Send a request of improvent and create a new draft version of the deal"
            )
          : this.$t(
              "Send a request of improvent and create a new draft version of the investor"
            ),
      submit_for_activation_link_title:
        this.otype === "deal"
          ? this.$t("Submits the deal for activation")
          : this.$t("Submits the investor for activation"),
      submit_to_delete_title:
        !this.objectVersion && this.object.status === 4
          ? this.otype === "deal"
            ? this.$t("Undelete deal")
            : this.$t("Undelete investor")
          : this.otype === "deal"
          ? this.$t("Delete deal")
          : this.$t("Delete investor"),
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
  computed: {
    last_revision() {
      return this.object?.versions[0]?.revision ?? "";
    },
    is_editable() {
      // object ist deleted
      if (!this.objectVersion && this.object.status === 4) return false;
      if (this.is_active_with_draft) return false;
      return this.is_authorized(this.object);
    },
    is_deletable() {
      if (this.is_active_with_draft) return false;
      if (this.is_old_draft) return false;
      return this.is_authorized(this.object);
    },
    is_deleted() {
      // active and deleted
      return !this.objectVersion && this.object.status === 4;
    },
    is_active_with_draft() {
      return !this.objectVersion && this.object.draft_status;
    },
    is_draft_with_active() {
      // current draft with active object
      if (this.objectVersion && [2, 3].includes(this.object.status)) return true;
      // old draft with activated object
      return this.is_old_draft && [2, 3].includes(this.latest_object_version.status);
    },
    is_old_draft() {
      return this.objectVersion && this.last_revision.id !== +this.objectVersion;
    },
    has_newer_draft() {
      if (this.is_active_with_draft) return true;
      // old with newer draft
      return this.is_old_draft && this.latest_object_version.draft_status;
    },
    has_active() {
      return !!this.object.status;
    },
    latest_object_version() {
      return this.object.versions.find((v) => v.revision.id === this.last_revision.id)[
        this.otype
      ];
    },
    get_edit_description() {
      if (this.object.draft_status === 1) {
        if (!this.has_active) {
          // only for new drafts without active
          return this.otype === "deal"
            ? this.$t("Starts editing this deal")
            : this.$t("Starts editing this investor");
        } else {
          // only for new drafts with active
          return this.otype === "deal"
            ? this.$t("Edits this draft version")
            : this.$t("Edits this investor version");
        }
      } else
        return this.otype === "deal"
          ? this.$t("Creates a new draft version of this deal")
          : this.$t("Creates a new draft version of this investor");
    },
    get_delete_text() {
      if (this.is_deleted) return this.$t("Undelete");
      else if (!this.objectVersion && !this.object.draft_status) {
        // active without draft
        return this.otype === "deal"
          ? this.$t("Delete deal")
          : this.$t("Delete investor");
      } else return this.$t("Delete");
    },
    get_delete_description() {
      if (this.is_deleted)
        return this.otype === "deal"
          ? this.$t("Undelete this deal as active deal")
          : this.$t("Undelete this investor as active investor");
      if (this.objectVersion && this.has_active) {
        // is draft and has active
        return this.otype === "deal"
          ? this.$t("Deletes this draft version of the deal")
          : this.$t("Deletes this draft version of the investor");
      } else
        return this.otype === "deal"
          ? this.$t("Deletes this deal")
          : this.$t("Deletes this investor");
    },
    get_activate_description() {
      return this.has_active
        ? this.$t("Activates submitted version replacing currently active version")
        : this.otype === "deal"
        ? this.$t("Sets the deal active")
        : this.$t("Sets the investor active");
    },
    transition_to_user() {
      let latest_draft_creation = this.object.workflowinfos.find((v) => {
        return !v.draft_status_before && v.draft_status_after === 1;
      });
      return latest_draft_creation.from_user;
    },
  },
  methods: {
    object_detail_path(obID, obV) {
      return this.otype === "deal"
        ? {
            name: "deal_detail",
            params: { dealId: obID, dealVersion: obV },
          }
        : {
            name: "investor_detail",
            params: { investorId: obID, investorVersion: obV },
          };
    },
    object_edit_path(obID, obV) {
      return this.otype === "deal"
        ? {
            name: "deal_edit",
            params: { dealId: obID, dealVersion: obV },
          }
        : {
            name: "investor_edit",
            params: { investorId: obID, investorVersion: obV },
          };
    },
    object_compare_path(oID, fromVersion, toVersion) {
      return this.otype === "deal"
        ? {
            name: "deal_compare",
            params: { dealId: oID, fromVersion, toVersion },
          }
        : {
            name: "investor_compare",
            params: { investorId: oID, fromVersion, toVersion },
          };
    },
    do_delete({ comment }) {
      this.$emit("delete", comment);
      this.show_to_delete_overlay = false;
    },
    do_to_draft({ comment, to_user }) {
      this.$emit("change_status", { transition: "TO_DRAFT", comment, to_user });
      this.show_to_draft_overlay = false;
    },
  },
};
export default ManageHeaderMixin;
