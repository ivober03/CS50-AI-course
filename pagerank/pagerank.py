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

    # Create an empty dictionary to store probabilities
    probabilities = {}

    # Get the set of pages linked to the current page, if there is none, consider it as having links to all pages
    linked_pages = corpus[page] if page in corpus else corpus

    # Calculate the probability of chosing a random page
    random_probability = (1 - damping_factor) / len(corpus)

    # If the page has outgoing links
    if linked_pages:

        # Calculate the probability of chosing a link
        link_probability = damping_factor / len(linked_pages)

        # Iterate through each page in the corpus and initialize its probability
        for linked_page in linked_pages:
        # For each page add damping_factor / linked_pages to its probability
            probabilities[linked_page] = link_probability + random_probability

    # If the page has not outgoing links then set equal probability to all pages
    else:
        for page in corpus:
            probabilities[page] = 1 / len(corpus)

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to the transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1).
    """

    # Create a dictionary to store PageRank values
    pagerank = {page: 0 for page in corpus}

    # Create a list to store samples
    samples = []

    # Pick the first sample randomly
    initial_sample = random.choice(list(corpus.keys()))

    # Store the first sample
    samples.append(initial_sample)

    # For each remaining sample
    for i in range(n - 1):
        # Use the transition model function to get the probabilities for the next sample
        transition_probabilities = transition_model(corpus, initial_sample, damping_factor)

        # Generate a random number between 0 and 1 to represent the stochastic behavior
        random_number = random.uniform(0, 1)

        # Initialize a cumulative probability counter
        cumulative_probability = 0

        # Iterate through the pages and their probabilities
        for page, probability in transition_probabilities.items():
            # Update the cumulative_probability by adding the current probability
            cumulative_probability += probability

            # Check if the random number falls in the cumulative_probability range and select the next page
            if random_number <= cumulative_probability:
                next_sample = page
                break  # Exit the loop once the next page is selected

        # Append the next sample to the list of samples
        samples.append(next_sample)

        # Update the PageRank value for the selected page
        pagerank[next_sample] += 1

        # Update the initial sample for the next iteration
        initial_sample = next_sample

    # Normalize the PageRank values by dividing them by the total number of samples
    total_samples = len(samples)
    pagerank = {page: rank / total_samples for page, rank in pagerank.items()}

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize pagerank values equal for all pages in corpus
    pagerank = {page: 1 / len(corpus) for page in corpus}

    total_pages = len(corpus)
    threshold = 0.001

    while True:
        new_pagerank = {page: 0 for page in corpus}
        convergence = True

        for page in corpus:
            # Calculate the part not influenced by links
            new_pagerank[page] = (1 - damping_factor) / total_pages

            for linking_page in corpus:
                if page in corpus[linking_page]:
                    # Update the PageRank based on linked pages
                    new_pagerank[page] += damping_factor * (pagerank[linking_page]) / len(corpus[linking_page])

            # Check for convergence
            if abs(new_pagerank[page] - pagerank[page]) > threshold:
                convergence = False

        if convergence:
            break

        pagerank = new_pagerank

    return pagerank

if __name__ == "__main__":
    main()
