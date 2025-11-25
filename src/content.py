import os
import pandoc
import pandoc.types as pt
from pathlib import Path

CONTENT_ENTRIES_DIRECTORY = "content/entries"


class ContentMetadata:
    title: str
    description: str
    pub_date: str
    edit_date: str | None
    tags: list[str]
    group: str
    visible: bool
    draft: bool


def parse_meta(meta: pt.Meta) -> ContentMetadata:
    """Parse pandoc metadata into ContentMetadata"""

    kvs = meta[0]
    cmd = ContentMetadata()
    stringify_list = lambda xs: [stringify(x) for x in xs]

    def stringify(item) -> str:
        match item:
            case pt.MetaInlines(inlines):
                return "".join([stringify(item) for item in inlines])
            case pt.Str(s):
                return s
            case pt.Space():
                return " "
            case pt.SoftBreak():
                return "\n"
            case pt.LineBreak():
                return "\n"
            case _:
                return ""

    required = {
        "title",
        "description",
        "pub_date",
    }

    mappings = {
        "title": stringify,
        "description": stringify,
        "pub_date": stringify,
        "edit_date": stringify,
        "tags": lambda x: stringify_list(x) if isinstance(x, pt.MetaList) else [],
        "group": stringify,
    }

    for key in required:
        if key not in kvs.keys():
            raise Exception(f"Missing required metadata key: {key}")

    [
        setattr(cmd, key, mappings[key](value))
        for key, value in kvs.items()
        if key in mappings
    ]

    return cmd


def template(metadata: ContentMetadata, name: str, body: str) -> str:
    template_str = (
        Path(Path(__file__).parent / "templates" / name)
        .with_suffix(".html")
        .read_text()
    )

    return template_str.format(
        title=metadata.title,
        body=body,
    )


def register(db):
    for filename in os.listdir(CONTENT_ENTRIES_DIRECTORY):
        if filename.endswith(".md"):
            slug = filename[:-3]
            filepath = os.path.join(CONTENT_ENTRIES_DIRECTORY, filename)
            entry = db.get_entry_by_slug(slug)

            if entry is None:
                content = Path(filepath).read_text()
                doc = pandoc.read(content)

                if doc[0] and not isinstance(doc[0], pt.Meta):
                    raise Exception(f"Missing metadata in {filename}")

                metadata = parse_meta(doc[0])
                body = template(metadata, "e", pandoc.write(doc, format="html"))

                db.insert_entry(
                    slug=slug,
                    body=body,
                    content_md5_hash="meow",
                    user_title=metadata.title if metadata else None,
                    user_description=metadata.description,
                    user_group=metadata.group,
                    user_date_created=metadata.pub_date,
                    user_date_modified=metadata.edit_date,
                    user_visibility="public",
                    user_draft=0,
                )
