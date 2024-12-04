# Block Alignment

## Introduction

In DNA alignment, "block alignment" is a technique that divides sequences into smaller segments, or "blocks" and focuses on comparing the similarities within these blocks rather than analyzing the entire sequence as a whole. This method helps identify conserved regions, even in highly divergent sequences, by emphasizing the presence or absence of specific patterns within the blocks, without regard to their exact order in the sequence. In this repo, we focus on how block alignment can speed up alignment process than the global alignment in terms of computation time.

## Methods

```
Algorithm:
  precompute()
  generate_permutations()
  generate_weight_alignments()
  compute_block_alignment()
```

- `precompute()`: In the precompute stage, we will load in words to be aligned, and deciding the length of the block which is definied as $\frac{1}{2}log_{|\sum|}^{n}$, where $n$ is the max length among words and $|\sum|$ is the number of distinct character among words.

- `generate_permutations()`: In the generate permutation stage, since we need to precompute all block combination with length of $t$. The first step is to generate all possible permutation for each block with length of $t$.  For example by given $\sum =$ {A,B,C} with $t = 2$, we will get {AA, AB, AC, BA, BB, BC, CA, CB, CC} which will be used in to following step to compute block weight alignment.

- `generate_weight_alignments()`: In the generate weight alignments stage we will build up a look up table with all possible combination with blocks with length $t$. In order to compute all combination of blocks in an efficient way, we will call another helper function called `compute_weight_alignment()` to compute any pair of block's alignmnet score. We apply space efficieny algorithm inside the `compute_weight_alignment()`. Here is the quick explanation for space efficieny algorithm: When computing the alignment score, we actually build up a dynamic programming table with size $n * m$ where n is the size of one word and m is the size of the other word. This imply that we have to store whole table (which is required if we want to backtrack for the path). However, we don't care about the path but only the find score in our case. Therefore, we can only keep the current 2 rows in our table to compute for the final score (Please see `compute_weight_alignment()` in `blockalignment.py` for detail explanation).

- `compute_block_alignment()`: 
