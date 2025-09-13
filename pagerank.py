import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # This dictionary will store the final probabilities
    model = {}

    # Get the set of links from the current page
    links = corpus[page]

    # Total number of pages in the corpus
    total_pages = len(corpus)

    # If the page has at least one link
    if links:
        for p in corpus:
            # Base probability from random jump
            model[p] = (1 - damping_factor) / total_pages

            # Add link-following probability if the page is linked
            if p in links:
                model[p] += damping_factor / len(links)
    else:
        # If the page has no links, treat it as linking to all pages
        for p in corpus:
            model[p] = 1 / total_pages

    return model
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Step 1: Initialize rank counts for each page to 0
    page_ranks = {}
    for page in corpus:
        page_ranks[page] = 0

    # Step 2: Choose a random starting page
    pages = list(corpus.keys())
    current_page = random.choice(pages)

    # Step 3: Repeat n times
    for i in range(n):
        # Step 3a: Count the current page visit
        page_ranks[current_page] += 1

        # Step 3b: Get the next page using the transition model
        model = transition_model(corpus, current_page, damping_factor)

        # Step 3c: Pick the next page based on the probabilities
        next_pages = list(model.keys())
        probabilities = list(model.values())
        current_page = random.choices(next_pages, weights=probabilities, k=1)[0]

    # Step 4: Convert counts to probabilities (normalize)
    for page in page_ranks:
        page_ranks[page] /= n

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
# Step 1: Set a small threshold for when to stop
    threshold = 0.001

    # Step 2: Total number of pages
    total_pages = len(corpus)

    # Step 3: Start with equal PageRank for each page
    pageranks = {}
    for page in corpus:
        pageranks[page] = 1 / total_pages

    # Step 4: Repeat until ranks converge
    while True:
        new_ranks = {}
        for page in corpus:
            # Start with the random jump part
            new_rank = (1 - damping_factor) / total_pages

            # Now add the contributions from all other pages
            for other_page in corpus:
                if page in corpus[other_page]:
                    # If other_page links to page
                    num_links = len(corpus[other_page])
                    if num_links != 0:
                        new_rank += damping_factor * (pageranks[other_page] / num_links)
                elif len(corpus[other_page]) == 0:
                    # Treat pages with no links as linking to all pages
                    new_rank += damping_factor * (pageranks[other_page] / total_pages)

            new_ranks[page] = new_rank

        # Step 5: Check for convergence (if ranks changed very little)
        changes = 0
        for page in pageranks:
            diff = abs(pageranks[page] - new_ranks[page])
            if diff > threshold:
                changes += 1

        pageranks = new_ranks

        # If all pages changed less than the threshold, stop
        if changes == 0:
            break

    return pageranks


if __name__ == "__main__":
    main()
