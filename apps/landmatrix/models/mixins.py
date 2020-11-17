import warnings

import reversion


class UnderscoreDisplayParseMixin:
    """ This mixin will help to convert `_display` to the corresponding values """

    def __getattribute__(self, attr):
        if attr.endswith("_display") and not attr.startswith("get_"):
            if hasattr(self, f"get_{attr}"):
                field = self.__getattribute__(f"get_{attr}")
                return field() if field else None
            else:
                return self.get_arrayfield_display(attr[:-8])
        return super().__getattribute__(attr)

    def get_arrayfield_display(self, name):
        choices = self._meta.get_field(name).base_field.choices
        vals = self.__getattribute__(name)
        if vals:
            return [dict(choices)[v] for v in vals]
        return


class ReversionSaveMixin:
    STATUS_DRAFT = 1
    STATUS_LIVE = 2
    STATUS_UPDATED = 3
    STATUS_DELETED = 4

    DRAFT_STATUS_DRAFT = 1
    DRAFT_STATUS_REVIEW = 2
    DRAFT_STATUS_ACTIVATION = 3
    DRAFT_STATUS_REJECTED = 4
    DRAFT_STATUS_TO_DELETE = 5

    def save_revision(self, status, date=None, user=None, comment=None):
        try:
            current_model = self.__class__.objects.get(pk=self.pk)
        except self.__class__.DoesNotExist:
            current_model = None

        # "Pending"
        if status == 1:
            if current_model:
                new_status = current_model.status
            else:
                new_status = self.STATUS_DRAFT
            new_draft_status = self.DRAFT_STATUS_DRAFT

        # "Active" and "Overwritten"
        elif status in [2, 3]:
            if current_model and current_model.status != self.STATUS_DRAFT:
                new_status = self.STATUS_UPDATED
            else:
                new_status = self.STATUS_LIVE
            new_draft_status = None

        # "Deleted"
        elif status == 4:
            new_status = self.STATUS_DELETED
            new_draft_status = None

        # "Rejected"
        elif status == 5:
            if current_model:
                new_status = current_model.status
            else:
                new_status = self.STATUS_DRAFT
            new_draft_status = self.DRAFT_STATUS_REJECTED

        # "To Delete"
        elif status == 6:
            if current_model:
                new_status = current_model.status
            else:
                new_status = self.STATUS_DRAFT
            new_draft_status = self.DRAFT_STATUS_TO_DELETE

        else:
            raise Exception("status must be between 1 and 6")

        with reversion.create_revision():
            self.status = new_status
            self.draft_status = new_draft_status

            reversion.add_to_revision(self)
            if date:
                reversion.set_date_created(date)
            if user:
                reversion.set_user(user)
            if comment:
                reversion.set_comment(comment)

            # save the actual model
            # if: there is not a current_model
            # or: there is a current model but it's a draft
            # or: the new status is Live, Updated or Deleted
            if (
                not current_model
                or (current_model.status == self.STATUS_DRAFT)
                or status in [2, 3, 4]
            ):
                self.save(custom_modification_date=date)
            # otherwise update the draft_status of the current_model
            else:
                self.__class__.objects.filter(pk=self.pk).update(
                    draft_status=new_draft_status
                )


unclear_fields = [
    # Ingore these.
    "Remark (Benefits for local communities)",  # an kurt geben
    "Remark (Nature of the deal)",
    "Remark (Number of Jobs Created)",
    "original_filename",
    "old_reliability_ranking",
    "timestamp",
    "minerals_export",  # weg. https://landmatrix.org/deal/6188/145156/
    "old_contract_area",  # weg. https://landmatrix.org/deal/4372/141302/
    "old_production_area",  # weg. https://landmatrix.org/deal/4372/141302/
    "previous_identifier",  # weg. Land Observatory Import History
    "terms",  # schmeissmer wir weg.
]

warnings.warn("GND Obsoletion Warning", FutureWarning)


class OldDealMixin:
    @staticmethod
    def old_attribute_names(key: str = None):
        old_values = {
            "general": [
                "target_country",
                "intended_size",
                "contract_size",
                "production_size",
                "tg_land_area_comment",
                "intention",
                "tg_intention_comment",
                "nature",
                "tg_nature_comment",
                "negotiation_status",
                "tg_negotiation_status_comment",
                "implementation_status",
                "tg_implementation_status_comment",
                "purchase_price",
                "purchase_price_currency",
                "purchase_price_type",
                "purchase_price_area",
                "tg_purchase_price_comment",
                "purchase_price_comment",  # alternative fuer tg_purchase_price_comment
                "annual_leasing_fee",
                "annual_leasing_fee_currency",
                "annual_leasing_fee_type",
                "annual_leasing_fee_area",
                "tg_leasing_fees_comment",
                "contract_farming",
                "on_the_lease",
                "on_the_lease_area",
                "on_the_lease_farmers",
                "on_the_lease_households",
                "off_the_lease",
                "off_the_lease_area",
                "off_the_lease_farmers",
                "off_the_lease_households",
                "tg_contract_farming_comment",
            ],
            "employment": [
                "total_jobs_created",
                "total_jobs_planned",
                "total_jobs_planned_employees",
                "total_jobs_planned_daily_workers",
                "total_jobs_current",
                "total_jobs_current_employees",
                "total_jobs_current_daily_workers",
                "tg_total_number_of_jobs_created_comment",
                "foreign_jobs_created",
                "foreign_jobs_planned",
                "foreign_jobs_planned_employees",
                "foreign_jobs_planned_daily_workers",
                "foreign_jobs_current",
                "foreign_jobs_current_employees",
                "foreign_jobs_current_daily_workers",
                "tg_foreign_jobs_created_comment",
                "domestic_jobs_created",
                "domestic_jobs_planned",
                "domestic_jobs_planned_employees",
                "domestic_jobs_planned_daily_workers",
                "domestic_jobs_current",
                "domestic_jobs_current_employees",
                "domestic_jobs_current_daily_workers",
                "tg_domestic_jobs_created_comment",
            ],
            "investor_info": [
                "operational_stakeholder",
                "actors",
                "project_name",
                "tg_operational_stakeholder_comment",
            ],
            "local_communities": [
                "name_of_community",
                "name_of_indigenous_people",
                "tg_affected_comment",
                "recognition_status",
                "tg_recognition_status_comment",
                "community_consultation",
                "tg_community_consultation_comment",
                "community_reaction",
                "tg_community_reaction_comment",
                "land_conflicts",
                "tg_land_conflicts_comment",
                "displacement_of_people",
                "number_of_displaced_people",
                "number_of_displaced_households",
                "number_of_people_displaced_from_community_land",
                "number_of_people_displaced_within_community_land",
                "number_of_households_displaced_from_fields",
                "number_of_people_displaced_on_completion",
                "tg_number_of_displaced_people_comment",
                "negative_impacts",
                "tg_negative_impacts_comment",
                "promised_compensation",
                "received_compensation",
                "promised_benefits",
                "tg_promised_benefits_comment",
                "materialized_benefits",
                "tg_materialized_benefits_comment",
                "presence_of_organizations",
            ],
            "former_use": [
                "land_owner",
                "tg_land_owner_comment",
                "land_use",
                "tg_land_use_comment",
                "land_cover",
                "tg_land_cover_comment",
            ],
            "produce_info": [
                "crops",
                "crops_yield",
                "crops_export",
                "tg_crops_comment",
                "animals",
                "animals_yield",
                "animals_export",
                "tg_animals_comment",
                "minerals",
                "minerals_yield",
                "export",
                "tg_minerals_comment",
                "contract_farming_crops",
                "tg_contract_farming_crops_comment",
                "contract_farming_animals",
                "tg_contract_farming_animals_comment",
                "has_domestic_use",
                "domestic_use",
                "has_export",
                "export_country1",
                "export_country1_ratio",
                "export_country2",
                "export_country2_ratio",
                "export_country3",
                "export_country3_ratio",
                "tg_use_of_produce_comment",
                "in_country_processing",
                "tg_in_country_processing_comment",
                "processing_facilities",
                "in_country_end_products",
            ],
            "water": [
                "water_extraction_envisaged",
                "tg_water_extraction_envisaged_comment",
                "source_of_water_extraction",
                "tg_source_of_water_extraction_comment",
                "tg_how_much_do_investors_pay_comment",
                "water_extraction_amount",
                "tg_water_extraction_amount_comment",
                "use_of_irrigation_infrastructure",
                "tg_use_of_irrigation_infrastructure_comment",
                "water_footprint",
            ],
            "remaining": [
                "tg_gender_specific_info_comment",
                "vggt_applied",
                "tg_vggt_applied_comment",
                "prai_applied",
                "tg_prai_applied_comment",
                "tg_overall_comment",
            ],
            "meta": [
                "fully_updated",
                "not_public",
                "not_public_reason",
                "tg_not_public_comment",
                "assign_to_user",  # TODO?
                "tg_feedback_comment",  # TODO?
            ],
        }
        if key:
            return old_values[key]
        return old_values


class OldLocationMixin:
    @staticmethod
    def old_attribute_names():
        return [
            "location",
            "location_description",
            "point_lat",
            "point_lon",
            "facility_name",
            "level_of_accuracy",
            "tg_location_comment",
            "contract_area",
            "intended_area",
            "production_area",
        ]


class OldContractMixin:
    @staticmethod
    def old_attribute_names():
        return [
            "contract_number",
            "contract_date",
            "contract_expiration_date",
            "agreement_duration",
            "tg_contract_comment",
        ]


class OldDataSourceMixin:
    @staticmethod
    def old_attribute_names():
        return [
            "type",
            "url",
            "file",
            "file_not_public",
            "publication_title",
            "date",
            "name",
            "company",
            "email",
            "phone",
            "includes_in_country_verified_information",
            "open_land_contracts_id",
            "tg_data_source_comment",
        ]
