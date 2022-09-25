# Error Tree 
The scripts are implementation of error tree algorithms for resolving the approximate matching problem. The full description is available at the preprint https://arxiv.org/pdf/2110.13802.pdf. 
Generally speaking, Pattern matching is a fundamental process in most scientific domains. The problem involves finding the starting positions of a given pattern (usually of short length) in a reference stream of data (of considerable length) as either exact or approximate (which allows for mismatches, insertions, or deletions) matching. For exact matching, several data structures built in linear time and space can be used in practice nowadays. The solutions proposed so far for approximate matching are non-linear, impractical, or heuristics. With the use of suffix trees and a tree structure derived from suffix trees, we designed and implemented a linear structure ($O(n)$) that resolves the approximate matching problem


-------------------------------------------------------------------------------- Prerequisite ---------------------------------------------------------------

Install the following library that will be used to build suffix trees:
https://github.com/ptrus/suffix-trees 

Then edit ./suffix_trees/STree.py as the followings:

- comment the following line, line 249, by inserting the character "#" at the beginning of the line. This will allow setting attributes to the suffix tree more freely.
```python
__slots__ = ['_suffix_link', 'transition_links', 'idx', 'depth', 'parent', 'generalized_idxs']
```

- In some procedures, we hashed internal nodes of suffix tree, to optimize this hashing we used only the combination of node index and node depth to identify uniquely an internal node instead of the original identification/naming of the nodes given by the library which is a bit long (shorter identification will use less space and speed up the lookup process for the hashed nodes. So replace the following two lines (which are line 264 and 265) 
```python
return ("SNode: idx:" + str(self.idx) + " depth:" + str(self.depth) +
                " transitons:" + str(list(self.transition_links.keys())))
```
with the line:
```python
return (str(self.idx) + "-" + str(self.depth))
```

-------------------------------------------------------------------------------- Preparation ----------------------------------------------------------------

Firstly, you need to convert the genome in fasta format to a one-line genome which remove any non A, C, G, T, and N (case is sensitive) and headers. This can be done using the script filter_DNA_file_to_4_bases_and_N.py by running the command:

```python
python3 Convert_fasta_file_to_4_bases_and_N.py $file.fasta > converted_fasta_file.DNA
```
-------------------------------------------------------------------------------- Running the tool -----------------------------------------------------------

The tool was tested on DNA sequences (fasta format). As a preparation process for the input data, remove headers and newlines from the fasta file so that all DNA sequence is stored in one line. The input for the tools is the converted fasta file. These tools are applicable for Hamming distance and Wildcards matching. Edit distance to be implemented.  

Running command:
```python
python3 {OT_index_script}.py converted_fasta_file.DNA k pattern 
```

- OT_index_script can be ET_using_base_paths.py or ET_using_base_suffixes.py.
- k value must be an integer.
- Pattern can be any sequence (for wildcards matching use a non {A,C,G,T,N} character).

As an example:
```python
python3 ET_using_base_paths.py converted_fasta_file.DNA 1 AAAAAAAAAAAAA
```

A sample output:
```
length of pattern 19
Reading input data took 0.00014 seconds
------------------------------------------------------------------------------------------
Building Suffix Tree took 0.41792 seconds
------------------------------------------------------------------------------------------
Number of internal nodes is 31627
Number of leaves is 47961
Processing leaf and internal nodes took 0.63112 seconds
------------------------------------------------------------------------------------------

***** Phase 1 for finding base suffixes finished in 0.46034 seconds
Length of OT index  426695
Left and right OT index of root 0 426695

***** Phase 2 for building OT index using base suffixes finished in 0.79204 seconds
Building OT index using base paths took 1.25245 seconds
------------------------------------------------------------------------
Approximate matchings for k value of  1
------------------------------------------------------------------------
GAAAAAAAAAAAAAAAAAA 1 [0] 157 leaf node
AGAAAAAAAAAAAAAAAAA 1 [1] 156 leaf node
AAGAAAAAAAAAAAAAAAA 1 [2] 155 leaf node
AAAGAAAAAAAAAAAAAAA 1 [3] 154 leaf node
AAAAAAAAAAAAAAAAAAT 1 [18] 184 leaf node

Number of matchings is 5
Number of position_combinations in the results 5
Number of expected combinations 19
All matching_results is with a distance equal to 1 as should be
All mismatches positions is equal to 1 as should be
------------------------------------------------------------------------
Approximate matchings for k value of  2
------------------------------------------------------------------------
TAAAGAAAAAAAAAAAAAA 2 [0, 4] 153 leaf node
AAAAAAAAAAAAAAAAATG 2 [17, 18] 185 leaf node

Number of matchings is 2
Number of position_combinations in the results 2
Number of expected combinations 171
All matching_results is with a distance equal to 2 as should be
All mismatches positions is equal to 2 as should be
------------------------------------------------------------------------
Approximate matchings for k value of  3
------------------------------------------------------------------------
TTAAAGAAAAAAAAAAAAA 3 [0, 1, 5] 152 leaf node
TAAAAAAATAAAAAAATAA 3 [0, 8, 19] 14975 leaf node
ATTAAAGAAAAAAAAAAAA 3 [1, 2, 6] 151 leaf node
ATAATAAAAAAAGAAAAAA 3 [1, 4, 13] 38898 leaf node
ATAAAAATAAAAATAAAAA 3 [1, 7, 13] 19781
ATAAAAATAAAAATAAAAA 3 [1, 7, 13] 19775
AATTAAAAAAAAAAACAAA 3 [2, 3, 19] 525 leaf node
AATAATAAAAAAAGAAAAA 3 [2, 5, 14] 38897 leaf node
AATAAAAATAAAAATAAAA 3 [2, 8, 14] 19780 leaf node
AAATTAAAAAAAAAAACAA 3 [3, 4, 20] 524 leaf node
AAATAATAAAAAAAGAAAA 3 [3, 6, 17] 38896 leaf node
AAATAAAAATAAAAATAAA 3 [3, 9, 15] 19779 leaf node
AAAATAAAAATAAAAATAA 3 [4, 10, 16] 19778 leaf node
AAAATAAAAATAAAAACAA 3 [4, 10, 16] 19784 leaf node
AAAAATAAAAATAAAAATA 3 [5, 11, 17] 19777 leaf node
AAAAATAAAAATAAAAACA 3 [5, 11, 17] 19783 leaf node
AAAAATAAAAAAGAAAGAA 3 [5, 12, 18] 47350 leaf node
AAAAAATAAAAAAGAAAGA 3 [6, 13, 19] 47349 leaf node
AAAAAAATAAAAAAATAAT 3 [7, 17, 20] 14976 leaf node
AAAAAAAAAAAAAAATGTA 3 [15, 16, 17] 187 leaf node
AAAAAAAAAAAAAAAATGT 3 [16, 17, 18] 186 leaf node

Number of matchings is 21
Number of position_combinations in the results 18
Number of expected combinations 969
All matching_results is with a distance equal to 3 as should be
All mismatches positions is equal to 3 as should be
Found approximate matching for k = 3 in  0.12331 seconds

```


For contact, please email AA.12682@KHCC.JO (the email of the first author Anas Al-okaily).
