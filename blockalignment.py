import math
import time
import pickle
import os

class BlockAlignment():
    def __init__(self):
        self.GAP_PENALTY = -2
        self.MISMATCH = -1
        self.MATCH = 1
        self.block_len = 0
        self.weighted_alignments = dict()

    def precompute(self, word1, word2):
        n = max(len(word1), len(word2))
        collection = set(word1 + word2)
        log_base = len(collection)
        new_block_len = round(math.log(n, log_base))//2

        if self.block_len != new_block_len:
            # new file path to read
            old_file_path = f'data/len_{self.block_len}.pkl'
            new_file_path = f'data/len_{new_block_len}.pkl'

            if old_file_path not in set(os.listdir('data')) and self.block_len != 0:
                with open(old_file_path, 'wb') as f:
                    pickle.dump(self.weighted_alignments, f)

            # load weighted alignments if there's any
            if new_file_path in set(os.listdir('data')):
                with open(new_file_path, 'rb') as f:
                    self.weighted_alignments.pickle.load(f)
            # otherwise, calculate new weighted alignments and save it to folder
            else:
                self.weighted_alignments = dict()
                self.block_len = new_block_len
                perm = self.generate_permutations(list(collection))
                self.generate_weight_alignments(perm)

                with open(new_file_path, 'wb') as f:
                    pickle.dump(self.weighted_alignments, f)


    def generate_weight_alignments(self, elements):
        """
        Update the self.weighted_alignments(value of each block) by calling compute_weight_alignment()
        This is one process of pre-computation

        Parameters
        ----------
        elements : list
            All permutations with length of self.block_len

        Returns
        -------
        None

        """
        for p1 in elements:
            for p2 in elements:
                if p1 == p2:
                    self.weighted_alignments[(p1,p2)] = len(p1)
                else:
                    k = sorted([p1,p2])
                    self.weighted_alignments[(k[0], k[1])] = self.compute_weight_alignment(k[0], k[1])


    def compute_weight_alignment(self, word1, word2):
        """
        Compute the actual weight alignment for each block (both word's length won't exceed self.block_len)
        This is one process of pre-computation

        Parameters
        ----------
        word1 : string
            word to be aligned
        word2 : string
            word to be aligned

        Returns
        -------
        score : int
            The final aligned score for 2 given words
        """

        # space efficieny algorithm
        siz1, siz2 = len(word1) + 1, len(word2) + 1
        first = [0 for _ in range(siz2)]

        for i in range(1, siz2):
            first[i] = first[i - 1] + self.GAP_PENALTY
    
        for i in range(siz1 - 1):
            second = [0 for _ in range(siz2)]
            second[0] = first[0] + self.GAP_PENALTY
            for j in range(1, siz2):
                if word1[i] == word2[j - 1]:
                    second[j] = max(second[j-1] + self.GAP_PENALTY, first[j] + self.GAP_PENALTY, first[j-1] + self.MATCH)
                else:
                    second[j] = max(second[j-1] + self.GAP_PENALTY, first[j] + self.GAP_PENALTY, first[j-1] + self.MISMATCH)
            first = second
        return second[-1]


    def generate_permutations(self, chars):
        """
        Generate all permutations with length self.block_len by the given collection of character

        Parameters
        ----------
        chars : list
            List of distinct character

        Returns
        -------
        List : list
            Distinct permutation from a given set with length of self.block_len
        """
        result = []
        
        def backtrack(current):
            if len(current) == self.block_len:
                # Once we reach block_len, yield the current permutation
                result.append(''.join(current))
                return
        
            for char in chars:
                # Add the next character and recurse
                backtrack(current + [char])
    
        # Start the recursion with an empty list
        backtrack([])
        return list(set(result))
        
    
    def compute_block_alignment(self, word1, word2):
        """
        Compute the block alignment with pre-comuted self.compute_weight_alignment

        Parameters
        ----------
        word1 : string
            word to be aligned
        word2 : string
            word to be aligned

        Returns
        -------
        score : int
            The final block aligned score for 2 given words
        """
        block1 = [word1[j:j + self.block_len] for j in range(0, len(word1), self.block_len)]
        block2 = [word2[j:j + self.block_len] for j in range(0, len(word2), self.block_len)]

        # add the remaining block whose size < block_len into the precompute matrix
        if len(block1[-1]) != self.block_len:
            for b2 in block2:
                k = sorted([block1[-1], b2])
                self.weighted_alignments[(k[0], k[1])] = self.compute_weight_alignment(k[0], k[1])
        
        if len(block2[-1]) != self.block_len:
            for b1 in block1:
                k = sorted([b1, block2[-1]])
                self.weighted_alignments[(k[0], k[1])] = self.compute_weight_alignment(k[0], k[1])

        # apply space efficieny algorithm
        siz1, siz2 = len(block1) + 1, len(block2) + 1
        first = [0 for _ in range(siz2)]

        for i in range(1,siz2):
            first[i] = first[i-1] + self.GAP_PENALTY * len(block2[i-1])

        for i in range(siz1-1):
            second = [0 for _ in range(siz2)]
            second[0] = first[0] + self.GAP_PENALTY * len(block1[i])
            for j in range(1, siz2):
                k = sorted([block2[j-1], block1[i]])
                second[j] = max(second[j-1] + self.GAP_PENALTY * 2, first[j] + self.GAP_PENALTY * 2, first[j-1] + self.weighted_alignments[(k[0], k[1])])
            
            first = second
        return second[-1]

    def block_align(self, word1, word2):
        self.precompute(word1, word2)
        start_time = time.time()
        
        score = self.compute_block_alignment(word1, word2)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return score, execution_time