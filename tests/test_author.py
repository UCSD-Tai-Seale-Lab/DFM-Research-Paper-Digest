"""
Tests Author class.
"""

from dfm_research_paper_digest import Author
from metapub import PubMedArticle, PubMedAuthor, PubMedFetcher


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
    assert author.slug == "Igor_V._Nikiforov"

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

    # Check matching of full middle names.
    assert different_pub_author.matches("Igor Igorovich Nikiforov")

    # Check matching of full middle name vs. other name initial only.
    assert different_pub_author.matches("Igor I. Nikiforov")

    # Last, first name style
    assert isinstance(author.pubmed_style, str)
    assert author.pubmed_style == "Nikiforov, Igor"


# Check we can catch corporate names without throwing exception.
def test_matching_corporate_names(pmid_with_corporate_author):
    author: Author = Author("Igor V. Nikiforov")
    assert isinstance(author, Author)

    # Test using string.
    assert not author.matches("NCI-Laboratories")

    # Test using PubMedAuthor object.
    fetcher: PubMedFetcher = PubMedFetcher()
    article: PubMedArticle = fetcher.article_by_pmid(pmid_with_corporate_author)
    corporate_author: PubMedAuthor = article.author_list[56]
    assert not author.matches(corporate_author)


def test_with_first_initials_only():
    author: Author = Author("Igor V. Nikiforov")
    assert isinstance(author, Author)
    assert author.matches("I. V. Nikiforov")
    assert not author.matches("Z. V. Nikiforov")
    assert not author.matches("Z. Nikiforov")


def test_with_accents():
    author: Author = Author("Ajayi, Toluwalase A., MD")
    assert isinstance(author, Author)
    assert author.matches("Tolúwalàṣẹ Àjàyí")
    assert author.matches("Àjàyí, T")


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
