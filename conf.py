# See the Documenteer docs for how to customize conf.py:
# https://documenteer.lsst.io/technotes/

from documenteer.conf.technote import *  # noqa F401 F403

# Make {cite:t} render as one link covering "Authors (Year)",
# instead of linking only the year.
from dataclasses import dataclass, field, fields

from sphinxcontrib.bibtex.plugin import register_plugin
from sphinxcontrib.bibtex.style.referencing import BracketStyle
from sphinxcontrib.bibtex.style.referencing.author_year import (
    AuthorYearReferenceStyle,
)
from sphinxcontrib.bibtex.style.referencing.basic_author_year import (
    BasicAuthorYearTextualReferenceStyle,
)
from sphinxcontrib.bibtex.style.template import (
    join,
    join2,
    post_text,
    pre_text,
    reference,
    year,
)


class LinkedTextualReferenceStyle(BasicAuthorYearTextualReferenceStyle):
    def inner(self, role_name):
        return reference[
            join(sep=self.text_reference_sep)[
                self.person.author_or_editor_or_title(full="s" in role_name),
                join[
                    self.bracket.left,
                    join2(sep1=self.pre_text_sep, sep2=self.post_text_sep)[
                        pre_text, year, post_text
                    ],
                    self.bracket.right,
                ],
            ]
        ]


@dataclass
class LinkedAuthorYearReferenceStyle(AuthorYearReferenceStyle):
    bracket_textual: BracketStyle = field(
        default_factory=lambda: BracketStyle(left="(", right=")")
    )

    def __post_init__(self):
        super().__post_init__()
        self.styles[:] = [
            LinkedTextualReferenceStyle(
                **{f.name: getattr(s, f.name) for f in fields(s)}
            )
            if type(s) is BasicAuthorYearTextualReferenceStyle
            else s
            for s in self.styles
        ]
        self.role_style.update(
            (role_name, style)
            for style in self.styles
            for role_name in style.role_names()
        )


register_plugin(
    "sphinxcontrib.bibtex.style.referencing",
    "author_year_linked",
    LinkedAuthorYearReferenceStyle,
)
bibtex_reference_style = "author_year_linked"
