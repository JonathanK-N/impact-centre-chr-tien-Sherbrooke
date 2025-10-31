"""Describe Firestore collection structure for future migration."""

FIRESTORE_MAPPING = {
    "users": {
        "document_id": "user_<id>",
        "fields": [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "postal_code",
            "country",
            "date_of_birth",
            "gender",
            "marital_status",
            "church_role",
            "membership_status",
            "role",
            "created_at",
            "updated_at",
        ],
        "subcollections": {
            "departments": "List of department_ids",
            "family": "Single family_id",
            "donations": "Donation documents",
            "events": "Participation records",
        },
    },
    "departments": {
        "fields": ["name", "description", "responsible_id", "created_at"],
        "subcollections": {
            "members": "user_ids",
            "announcements": "Annonces lies",
            "events": "Evenements lies",
        },
    },
    "families": {
        "fields": [
            "name",
            "description",
            "address",
            "city",
            "postal_code",
            "country",
            "meeting_day",
            "meeting_time",
            "latitude",
            "longitude",
            "responsible_id",
        ],
        "subcollections": {
            "members": "user_ids",
            "announcements": "Annonces lies",
            "events": "Evenements lies",
        },
    },
    "events": {
        "fields": [
            "title",
            "description",
            "start_at",
            "end_at",
            "location",
            "is_virtual",
            "max_attendees",
            "created_by",
            "department_id",
            "family_id",
        ],
        "subcollections": {"participants": "user_ids"},
    },
    "announcements": {
        "fields": [
            "title",
            "body",
            "scope",
            "author_id",
            "department_id",
            "family_id",
            "published_at",
            "expires_at",
        ]
    },
    "donations": {
        "fields": [
            "user_id",
            "amount",
            "currency",
            "payment_method",
            "status",
            "receipt_url",
            "created_at",
        ]
    },
    "media_items": {
        "fields": [
            "title",
            "description",
            "media_type",
            "url",
            "published_at",
            "tags",
            "department_id",
            "family_id",
        ]
    },
}
