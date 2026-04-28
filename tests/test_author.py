"""
Tests Author class.
"""

from src.dfm_research_paper_digest.author import Author


def test_author():
    """Tests instantiation of Author object."""
    author: Author = Author("Igor V. Nikiforov")
    assert isinstance(author, Author)

    assert author.first == "Igor"
    assert author.middle == "V."
    assert author.last == "Nikiforov"
    assert author.middle_initial_only
    assert author.middle_initial == "V"
    assert author.original == "Igor V. Nikiforov"

    # Check different first names fails.
    different_author: Author = Author("Craig Nikiforov")
    assert not author.matches(different_author)

    # Check different last names fails.
    yet_another_author: Author = Author("Igor Jones")
    assert not author.matches(yet_another_author)

    # Missing middle initial still matches.
    pub_author: Author = Author("Igor Nikiforov")
    assert author.matches(pub_author)

    # Different middle initial DOESN'T match.
    other_pub_author: Author = Author("Igor X. Nikiforov")
    assert not author.matches(other_pub_author)

    # Full name with matching initial matches.
    another_pub_author: Author = Author("Igor Vladimir Nikiforov")
    assert author.matches(another_pub_author)

    # Full name with different first initial DOESN'T match.
    different_pub_author: Author = Author("Igor Igorovich Nikiforov")
    assert not author.matches(different_pub_author)

    # Check matches against str.
    assert author.matches("Igor Vladimir Nikiforov")
    assert author

    # Last, first name style
    assert isinstance(author.pubmed_style, str)
    assert author.pubmed_style == "Nikiforov, Igor"


def test_matching_list():
    """Exercises matching an Author against a list."""
    # List of Authors
    author: Author = Author("Igor V. Nikiforov")
    author1: Author = Author("Adam A. Able")
    author2: Author = Author("Igor Nikiforov")
    author3: Author = Author("Brenda B. Bravo")
    assert author.matches([author1, author2, author3])
    assert not author.matches([author1, author3])

    # List of str
    assert author.matches(["Adam A. Able", "Igor Nikiforov", "Brenda B. Bravo"])
    assert not author.matches(["Adam A. Able", "Brenda B. Bravo"])
