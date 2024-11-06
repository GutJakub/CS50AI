import os
import random
import re
import sys
import copy
DAMPING = 0.85
SAMPLES = 10000


def main():
    print("Main start")
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
    trans_corpus={}
    for key,val in corpus.items():
        trans_corpus[key]=0

    lcount=len(corpus[page])
    for val in corpus[page]:
        trans_corpus[val]=damping_factor/lcount

    kcount=len(corpus.keys())    
    for key,val in trans_corpus.items():
        trans_corpus[key]+=(1-damping_factor)/kcount
    return trans_corpus
    #raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    start=random.choice(list(corpus.keys()))
    
    count_corpus={}
    for key,val in corpus.items():
        count_corpus[key]=0
    model=transition_model(corpus,start,damping_factor)
    for _ in range(n):
        page=random.choices(list(model.keys()),weights=list(model.values()),k=1)[0]
        count_corpus[page]+=1/10000
        model=transition_model(corpus,page,damping_factor)
        
    #print(count_corpus)
    return count_corpus
    #raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rc=dict()
    links=dict()
    for key,val in corpus.items():
        rc[key]=1/len(corpus.keys())
        links[key]=set()
        if val==set():
            corpus[key]=set(corpus.keys())
    for key,val in corpus.items():
        for link in val:
            links[link].add(key)

    while True:
        rc_primary=copy.deepcopy(rc)
        print(f"słownik {rc}")
        print(f" słownik kopia {rc}")
        
        for key,val in links.items():
            suma=0
            for link in val:
                suma+=rc[link]/len(corpus[link])
            rc[key]=(1-damping_factor)/len(corpus.keys())+damping_factor*suma
        diff=[abs(a-b) for a,b in zip(list(rc_primary.values()),list(rc.values()))]
        if all( d<0.001 for d in diff):
            break
    return rc
    # dodac handle dla bez linkowych stron




if __name__ == "__main__":
    main()
