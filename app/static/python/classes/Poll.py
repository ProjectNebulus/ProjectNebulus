from datetime import datetime

from mongoengine import (
    DateTimeField,
    EmbeddedDocument,
    ReferenceField,
    StringField,
    URLField,
    ValidationError,
)


class Poll(EmbeddedDocument):
    meta = {"collection": "Polls"}
    url = URLField(required=True)
    name = StringField(required=True)
    description = StringField(default="")
    upload_date = DateTimeField(default=lambda: datetime.now)
    folder = ReferenceField(
        "Folder", default=None, required=True
    )  # 0 if it's in the course, not any folder
    course = ReferenceField("Course", default=None, required=True)

    def clean(self):
        """
        Validates the Document.
        """
        if not self.url:
            self.url = f"https://nebulus-cdn.sfo3.cdn.digitaloceanspaces.com/Documents/{self.pk}"

        # Document should be linked to both course and folder. Folder is 0 if its in the root.
        if self.folder is None and self.course is None:
            raise ValidationError(
                "Document must be linked to either a folder or a course."
            )
