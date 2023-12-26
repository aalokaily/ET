from suffix_trees import STree 
from collections import defaultdict
import time
import math 
import sys
import bisect



print ("Building Suffix Tree")

def Build_suffix_tree():
    global tree
    
    input_file = sys.argv[1]    
    text = ""
    with open(input_file) as file_in:        
        for line in file_in:
            if line[0] != ">":
                text += line.strip()
                
    
    tree = STree.STree(text)
    
    
    
start = time.time()   
Build_suffix_tree()
print ("Finished in", round((time.time() - start), 5), "seconds")
print ("------------------------------------------------------------------------------------------")


print ("Processing leaf and internal nodes")
 
def process_leaf_and_internal_nodes(tree):    
    
    setattr(tree, "number_leaf_nodes", 0)
    setattr(tree, "number_internal_nodes", 0)
    setattr(tree, "List_of_left_to_right_suffix_indexes", []) # List S in the paper with minor modification
    setattr(tree, "List_of_leaf_suffix_index_to_leaf_memory", []) # List M in the paper 
     
    tree.List_of_leaf_suffix_index_to_leaf_memory = [-1] * len(tree.word)
    
    nodes_stack = []
    key_stack = []
    children_stack = []

    #iterative processing
    nodes_stack.append(tree.root)
    children_stack.append((list(tree.root.transition_links[x] for x in sorted(tree.root.transition_links.keys(), reverse=True))))
    
    while nodes_stack:
        current_visited_node = nodes_stack[-1]                  
        if len(children_stack[-1]) > 0:
            last_node_under_top_node_in_stack = children_stack[-1][-1]
            #iterative processing
            nodes_stack.append(last_node_under_top_node_in_stack)   # append it to process later with the required order (postorder) and remove it from OSHR[current_visited_node.key]
            children_stack[-1].pop()                    
            children_stack.append((list(last_node_under_top_node_in_stack.transition_links[x] for x in sorted(last_node_under_top_node_in_stack.transition_links.keys(), reverse=True))))
                                      
        else:
            setattr(current_visited_node, "OT_indexes", [])
            # alongside processing
            if current_visited_node.is_leaf():
                # Assigning leaf nodes unique keys
                current_visited_node.index_of_leaf_in_ST = tree.number_leaf_nodes                     
                tree.number_leaf_nodes += 1
                
                # creating auxiliary lists 
                tree.List_of_leaf_suffix_index_to_leaf_memory[current_visited_node.idx] = current_visited_node
                tree.List_of_left_to_right_suffix_indexes.append(current_visited_node.idx)
                
                if not hasattr(current_visited_node.parent, "index_of_leftmost_leaf_in_ST"):
                    setattr(current_visited_node.parent, "index_of_leftmost_leaf_in_ST", current_visited_node.index_of_leaf_in_ST)
                elif current_visited_node.index_of_leaf_in_ST < current_visited_node.parent.index_of_leftmost_leaf_in_ST:
                    current_visited_node.parent.index_of_leftmost_leaf_in_ST = current_visited_node.index_of_leaf_in_ST
                if not hasattr(current_visited_node.parent, "index_of_rightmost_leaf_in_ST"):
                    setattr(current_visited_node.parent, "index_of_rightmost_leaf_in_ST", current_visited_node.index_of_leaf_in_ST)
                elif current_visited_node.index_of_leaf_in_ST > current_visited_node.parent.index_of_rightmost_leaf_in_ST:
                    current_visited_node.parent.index_of_rightmost_leaf_in_ST = current_visited_node.index_of_leaf_in_ST
                    
            else:
                tree.number_internal_nodes += 1
                setattr(current_visited_node, "List_of_base_suffixes", [])  
                # construct implicit OSHR tree
                if current_visited_node._suffix_link is not None and current_visited_node != tree.root:
                    temp = current_visited_node._suffix_link
                    if not hasattr(temp, "List_of_nodes_suffix_linked_to_me"):
                        setattr(temp, "List_of_nodes_suffix_linked_to_me", [])
                    temp.List_of_nodes_suffix_linked_to_me.append(current_visited_node)
            
                if not hasattr(current_visited_node.parent, "index_of_leftmost_leaf_in_ST"):
                    setattr(current_visited_node.parent, "index_of_leftmost_leaf_in_ST", current_visited_node.index_of_leftmost_leaf_in_ST)
                elif current_visited_node.index_of_leftmost_leaf_in_ST < current_visited_node.parent.index_of_leftmost_leaf_in_ST:
                    current_visited_node.parent.index_of_leftmost_leaf_in_ST = current_visited_node.index_of_leftmost_leaf_in_ST
                if not hasattr(current_visited_node.parent, "index_of_rightmost_leaf_in_ST"):
                    setattr(current_visited_node.parent, "index_of_rightmost_leaf_in_ST", current_visited_node.index_of_rightmost_leaf_in_ST)
                elif current_visited_node.index_of_rightmost_leaf_in_ST > current_visited_node.parent.index_of_rightmost_leaf_in_ST:
                    current_visited_node.parent.index_of_rightmost_leaf_in_ST = current_visited_node.index_of_rightmost_leaf_in_ST
            
                
            #iterative processing 
            nodes_stack.pop()
            children_stack.pop()
            
    print ("Number of leaf nodes is", "{:,}".format(tree.number_leaf_nodes))
    print ("Number of internal nodes is", "{:,}".format(tree.number_internal_nodes))
    print ("Number of alphabets in the input data", len(tree.root.transition_links) - 1)



start = time.time()
process_leaf_and_internal_nodes(tree)
print ("Finished in", round((time.time() - start), 5), "seconds")
print ("------------------------------------------------------------------------------------------")
    
  
print ("Finding base suffixes using the linear algorithm")

def Find_base_suffixes_using_linear_algorithm(tree):
    # Note that reference leaf nodes and reference internal nodes will not be created explicitly as they will not be used by any process. However, in case a user 
    # may need them, the algorithm that create them explicitly is provided as supplemntary at the bottom of this script with name Find_base_suffixes_using_linear_algorithm2
    nodes_stack = []
    children_stack = []
    
    nodes_stack.append(tree.root)
    children_stack.append((list(tree.root.transition_links[x] for x in sorted(tree.root.transition_links.keys(), reverse=True))))       
    
    cost = 0
    OSHR_leaf_nodes_key_counter = 0
    OSHR_internal_nodes_key_counter = 0
    base_suffix_counter = 0
                    
    while nodes_stack:
        cost += 1
        current_visited_node = nodes_stack[-1]                  
        if len(children_stack[-1]) > 0:
            last_node_under_top_node_in_stack = children_stack[-1][-1]
            nodes_stack.append(last_node_under_top_node_in_stack)  

            children_stack[-1].pop()                    
            children_stack.append((list(last_node_under_top_node_in_stack.transition_links[x] for x in sorted(last_node_under_top_node_in_stack.transition_links.keys(), reverse=True))))                                          
        else:
            nodes_stack.pop()
            children_stack.pop()

            # alongside processing
            if current_visited_node.is_leaf():
                if current_visited_node.idx + 1 < tree.number_leaf_nodes:
                    # this code computes base suffixes derived from reference leaf nodes. 
                    leaf_node_of_next_suffix_index = tree.List_of_leaf_suffix_index_to_leaf_memory[current_visited_node.idx + 1]                                    
                    if leaf_node_of_next_suffix_index.parent != current_visited_node.parent._suffix_link:
                        temp = leaf_node_of_next_suffix_index.parent
                        end_node = current_visited_node.parent._suffix_link
                        while True:
                            cost += 1
                            if temp == end_node:
                                if current_visited_node.parent == tree.root: # if so, then we must add this suffix as a base suffix to end_node unlike other cases (end_node must be tree.root)
                                    temp.List_of_base_suffixes.append(leaf_node_of_next_suffix_index.idx + temp.depth) 
                                    base_suffix_counter += 1 
                                break
                            else:
                                temp.List_of_base_suffixes.append(leaf_node_of_next_suffix_index.idx + temp.depth)
                                temp = temp.parent
                                base_suffix_counter += 1
                            
            else:
                # this code computes base suffixes derived from reference internal nodes.
                if current_visited_node._suffix_link.parent != current_visited_node.parent._suffix_link:
                    top_node = current_visited_node.parent._suffix_link 
                    bottom_node = current_visited_node._suffix_link

                    temp = bottom_node.parent
                    while temp != top_node:
                        cost += 1
                        for suffix_index_of_leaf_node in tree.List_of_left_to_right_suffix_indexes[current_visited_node.index_of_leftmost_leaf_in_ST:current_visited_node.index_of_rightmost_leaf_in_ST + 1]:
                            temp.List_of_base_suffixes.append(suffix_index_of_leaf_node + 1 + temp.depth)
                            base_suffix_counter += 1
                        temp = temp.parent
                        
                
                if hasattr(current_visited_node, "List_of_nodes_suffix_linked_to_me"):
                    OSHR_internal_nodes_key_counter += 1
                else:
                    OSHR_leaf_nodes_key_counter += 1       
                

    # compute the case for suffix 0 as there is no previous index for index 0 
    cost += 1
    temp = tree.List_of_leaf_suffix_index_to_leaf_memory[0]                                     
    while temp != tree.root:
        temp = temp.parent
        temp.List_of_base_suffixes.append(0 + temp.depth)
        base_suffix_counter += 1
        cost += 1
        
        
    # this a special cases and for the root only. The suffix-link of child internal node of a root usually link to the root. In case not, 
    # then the node that the child internal node link to must be bottom-node for the root node.
    cost += 1
    current_visited_node = tree.root
    for node in current_visited_node.transition_links.values():
        cost += 1
        if node.is_leaf():
            if node.idx + 1 < tree.number_leaf_nodes:
                leaf_node_of_next_suffix_index = tree.List_of_leaf_suffix_index_to_leaf_memory[node.idx + 1]
                if leaf_node_of_next_suffix_index.parent == tree.root:
                    current_visited_node.List_of_base_suffixes.append(leaf_node_of_next_suffix_index.idx)
                    base_suffix_counter += 1
        else:
            if node._suffix_link != tree.root:
                for suffix_index_of_leaf_node in tree.List_of_left_to_right_suffix_indexes[node.index_of_leftmost_leaf_in_ST:node.index_of_rightmost_leaf_in_ST + 1]:
                    current_visited_node.List_of_base_suffixes.append(suffix_index_of_leaf_node + 1)
                    base_suffix_counter += 1
                    cost += 1
    
       
    print ("Number of OSHR leaf_nodes is", "{:,}".format(OSHR_leaf_nodes_key_counter))
    print ("Number of OSHR internal nodes is", "{:,}".format(OSHR_internal_nodes_key_counter))
    print ("Total number of base suffixes", "{:,}".format(base_suffix_counter))
    print ("Total time cost:", "{:,}".format(cost))

   

start = time.time()
Find_base_suffixes_using_linear_algorithm(tree)
print ("Finished in", round((time.time() - start), 5), "seconds")
print ("------------------------------------------------------------------------------------------")
    

print ("Finding and checking base suffixes using the non-trivial algorithm 1 and O(n) space (hash-table)")

def Find_and_check_base_suffixes_using_non_trivial_algorithm1(tree):
    
    setattr(tree, "All_base_suffixes_found_so_far", defaultdict())
    cost = 0
    flag = 0
    
    nodes_stack = []
    children_stack = []
    
    nodes_stack.append(tree.root)
    children_stack.append((list(tree.root.List_of_nodes_suffix_linked_to_me)))

    while nodes_stack:
        cost += 1
        current_visited_node = nodes_stack[-1]    
        # check if OSHR[current_visited_node] is empty, then remove it from nodes_stack
        if len(children_stack[-1]) > 0:
            last_node_under_top_node_in_stack = children_stack[-1][-1]
            nodes_stack.append(last_node_under_top_node_in_stack)     
            children_stack[-1].pop()
            if hasattr(last_node_under_top_node_in_stack, "List_of_nodes_suffix_linked_to_me"):
                children_stack.append((list(last_node_under_top_node_in_stack.List_of_nodes_suffix_linked_to_me)))
            else:
                children_stack.append([])
        else:
            if not current_visited_node.is_leaf():
                d = []
                if hasattr(current_visited_node, "List_of_nodes_suffix_linked_to_me"):
                    for suffix_index_of_leaf_node in tree.List_of_left_to_right_suffix_indexes[current_visited_node.index_of_leftmost_leaf_in_ST:current_visited_node.index_of_rightmost_leaf_in_ST + 1]:
                        cost += 1
                        if suffix_index_of_leaf_node + current_visited_node.depth not in tree.All_base_suffixes_found_so_far:
                            d.append(suffix_index_of_leaf_node + current_visited_node.depth)
                            tree.All_base_suffixes_found_so_far[suffix_index_of_leaf_node + current_visited_node.depth] = 0
                    
                else:
                    setattr(current_visited_node, "All_suffixes_under_node", defaultdict())
                    for suffix_index_of_leaf_node in tree.List_of_left_to_right_suffix_indexes[current_visited_node.index_of_leftmost_leaf_in_ST:current_visited_node.index_of_rightmost_leaf_in_ST + 1]:
                        cost += 1
                        tree.All_base_suffixes_found_so_far[suffix_index_of_leaf_node + current_visited_node.depth] = 0
                        d.append(suffix_index_of_leaf_node + current_visited_node.depth)

                        
                #if sorted(d) != sorted(current_visited_node.List_of_base_suffixes):
                #    print ("The two base suffixes lists of this internal node are different", current_visited_node, sorted(d), sorted(current_visited_node.List_of_base_suffixes))   
                #    flag = 1
             
            
            nodes_stack.pop()
            children_stack.pop()
    
    if flag == 0:
        print ("=== All base suffixes at each internal nodes in ST are as expected ===")
        print ("Total time cost:", "{:,}".format(cost))
    else:
        print ("*** There are base suffixes lists that are different at some internal nodes***")
    
    
start = time.time()    
Find_and_check_base_suffixes_using_non_trivial_algorithm1(tree)
print ("Finished in", round((time.time() - start), 5), "seconds")
print ("------------------------------------------------------------------------------------------")


 
print ("Finding and checking base suffixes using the non-trivial algorithm 2 with additional log(Sigma) time factor")

def Find_and_check_base_suffixes_using_non_trivial_algorithm2(tree):
    
    print ("Sorting nodes link through suffix-links to each node in ST")
    
    nodes_stack = []
    children_stack = []
    
    cost = 0
    
    #iterative processing
    nodes_stack.append(tree.root)
    children_stack.append((list(tree.root.transition_links[x] for x in sorted(tree.root.transition_links.keys(), reverse=True))))
    
    while nodes_stack:
        cost += 1
        current_visited_node = nodes_stack[-1]                
        if len(children_stack[-1]) > 0:
            last_node_under_top_node_in_stack = children_stack[-1][-1]
            #iterative processing
            nodes_stack.append(last_node_under_top_node_in_stack)     # append it to process later with the required order (postorder) and remove it from OSHR[current_visited_node.key]
            children_stack[-1].pop()                    
            children_stack.append((list(last_node_under_top_node_in_stack.transition_links[x] for x in sorted(last_node_under_top_node_in_stack.transition_links.keys(), reverse=True))))
        else:
            # alongside processing
            if not current_visited_node.is_leaf():
                if hasattr(current_visited_node, "List_of_nodes_suffix_linked_to_me"):
                    # The follwing new list will be needed in next phase
                    setattr(current_visited_node, "List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST", [])
                    for node in current_visited_node.List_of_nodes_suffix_linked_to_me:
                        current_visited_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST.append((node.index_of_leftmost_leaf_in_ST, node.index_of_rightmost_leaf_in_ST, node))
                        cost += 1
                    current_visited_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST.sort(key=lambda element: (element[0], element[1]))
                
            #iterative processing
            nodes_stack.pop()
            children_stack.pop()
    
    
    print ("Cost for sorting all List_of_nodes_suffix_linked_to_me", "{:,}".format(cost))
    
    # --------------------------------------------------------------------------- find base suffixes -------------------------------------------
    print ("Finding base suffixes")
    
    nodes_stack = []
    children_stack = []
    
    flag = 0
    nodes_stack.append(tree.root)
    children_stack.append((list(tree.root.List_of_nodes_suffix_linked_to_me)))

    while nodes_stack:
        current_visited_node = nodes_stack[-1]    
        # check if OSHR[current_visited_node] is empty, then remove it from nodes_stack
        if len(children_stack[-1]) > 0:
            last_node_under_top_node_in_stack = children_stack[-1][-1]
            nodes_stack.append(last_node_under_top_node_in_stack)     
            children_stack[-1].pop()
            if hasattr(last_node_under_top_node_in_stack, "List_of_nodes_suffix_linked_to_me"):
                children_stack.append((list(last_node_under_top_node_in_stack.List_of_nodes_suffix_linked_to_me)))
            else:
                children_stack.append([])

        else:
            cost += 1
            if not current_visited_node.is_leaf():
                d = []
                if hasattr(current_visited_node, "List_of_nodes_suffix_linked_to_me"):
                    for suffix_index_of_leaf_node in tree.List_of_left_to_right_suffix_indexes[current_visited_node.index_of_leftmost_leaf_in_ST:current_visited_node.index_of_rightmost_leaf_in_ST + 1]:
                        cost += int(math.log(len(current_visited_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST),2))
                        f = 0
                        leaf_node_of_previous_suffix_index = tree.List_of_leaf_suffix_index_to_leaf_memory[suffix_index_of_leaf_node - 1]
                        right_pos = bisect.bisect(current_visited_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST, (leaf_node_of_previous_suffix_index.index_of_leaf_in_ST, leaf_node_of_previous_suffix_index.index_of_leaf_in_ST)) # right_pos bcus we want to find node satisfies the condition starting_node.left_OT_index >= node.left_OT_index and starting_node.right_OT_index <= node.right_OT_index
                        if right_pos == len(current_visited_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST):
                            right_pos = right_pos - 1
                        node_suffix_link_to_current_visited_node = current_visited_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST[right_pos][2]
                        if node_suffix_link_to_current_visited_node.index_of_leftmost_leaf_in_ST <= leaf_node_of_previous_suffix_index.index_of_leaf_in_ST <= node_suffix_link_to_current_visited_node.index_of_rightmost_leaf_in_ST:
                            f = 1
                        else:
                            right_pos = right_pos - 1
                            node_suffix_link_to_current_visited_node = current_visited_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST[right_pos][2]
                            if node_suffix_link_to_current_visited_node.index_of_leftmost_leaf_in_ST <= leaf_node_of_previous_suffix_index.index_of_leaf_in_ST <= node_suffix_link_to_current_visited_node.index_of_rightmost_leaf_in_ST:
                                f = 1 
                        
                        if f == 0:
                            d.append(suffix_index_of_leaf_node + current_visited_node.depth)
                    
                else:
                    for suffix_index_of_leaf_node in tree.List_of_left_to_right_suffix_indexes[current_visited_node.index_of_leftmost_leaf_in_ST:current_visited_node.index_of_rightmost_leaf_in_ST + 1]:
                        cost += 1
                        d.append(suffix_index_of_leaf_node + current_visited_node.depth)

                        
                #if sorted(d) != sorted(current_visited_node.List_of_base_suffixes):
                #    print ("The two base suffixes lists of this internal node are different", current_visited_node, sorted(d), sorted(current_visited_node.List_of_base_suffixes))   
                #    flag = 1
                    
                        
                    
            nodes_stack.pop()
            children_stack.pop()

    if flag == 0:
        print ("=== All base suffixes at each internal nodes in ST are as expected ===")
        print ("Total time cost:", "{:,}".format(cost))
    else:
        print ("*** There are base suffixes lists that are different at some internal nodes***")
    
    
start = time.time()    
Find_and_check_base_suffixes_using_non_trivial_algorithm2(tree)
print ("Finished in", round((time.time() - start), 5), "seconds")








####### Not used: Algorithm for finding base suffixes using linear linear algorithm by creating explicitly reference leaf nodes and reference internal nodes (in case reference leaf nodes and reference internal nodes might be used)

def Find_base_suffixes_using_linear_algorithm2(tree):
    
    print ("Indexing reference_internal_nodes and reference_leaf_nodes")

    nodes_stack = []
    children_stack = []
    
    cost = 0
    OSHR_leaf_nodes_key_counter = 0
    OSHR_internal_nodes_key_counter = 0
    reference_internal_nodes = 0
    reference_leaf_nodes = 0

    #iterative processing
    nodes_stack.append(tree.root)
    children_stack.append((list(tree.root.transition_links[x] for x in sorted(tree.root.transition_links.keys(), reverse=True))))
    
    while nodes_stack:
        cost += 1
        current_visited_node = nodes_stack[-1]                
        if len(children_stack[-1]) > 0:
            last_node_under_top_node_in_stack = children_stack[-1][-1]
            #iterative processing
            nodes_stack.append(last_node_under_top_node_in_stack)     # append it to process later with the required order (postorder) and remove it from OSHR[current_visited_node.key]
            children_stack[-1].pop()                    
            children_stack.append((list(last_node_under_top_node_in_stack.transition_links[x] for x in sorted(last_node_under_top_node_in_stack.transition_links.keys(), reverse=True))))
        else:
            # alongside processing
            if current_visited_node.is_leaf():
                # this code to find reference leaf nodes
                if current_visited_node.idx + 1 < tree.number_leaf_nodes:
                    leaf_node_of_next_suffix_index = tree.List_of_leaf_suffix_index_to_leaf_memory[current_visited_node.idx + 1]                                    
                    if leaf_node_of_next_suffix_index.parent != current_visited_node.parent._suffix_link:
                        n = leaf_node_of_next_suffix_index.parent
                        top_node = current_visited_node.parent._suffix_link
                        
                        while True:
                            cost += 1
                            if n == top_node:
                                if current_visited_node.parent == tree.root: # if so, then we must add this suffix as a base suffix to top_node unlike other cases (top_node must be tree.root)
                                    if not hasattr(n, "List_of_reference_leaf_nodes"):
                                        setattr(n, "List_of_reference_leaf_nodes", [])
                                    n.List_of_reference_leaf_nodes.append(current_visited_node)
                                    reference_leaf_nodes += 1
                                break
                            else:
                                if not hasattr(n, "List_of_reference_leaf_nodes"):
                                    setattr(n, "List_of_reference_leaf_nodes", [])
                                n.List_of_reference_leaf_nodes.append(current_visited_node)
                                n = n.parent
                                reference_leaf_nodes += 1

            else:
                #find and mark inbetween top base node and assign the reference nodes for this node (which are as coded below)
                if current_visited_node._suffix_link.parent != current_visited_node.parent._suffix_link:
                    top_node = current_visited_node.parent._suffix_link 
                    bottom_node = current_visited_node._suffix_link

                    n = bottom_node.parent
                    while n != top_node:
                        cost += 1
                        if not hasattr(n, "List_of_reference_internal_nodes"):
                            setattr(n, "List_of_reference_internal_nodes", [])
                        n.List_of_reference_internal_nodes.append(current_visited_node)
                        n = n.parent
                        reference_internal_nodes += 1

                if hasattr(current_visited_node, "List_of_nodes_suffix_linked_to_me"):
                    OSHR_internal_nodes_key_counter += 1
                else:
                    OSHR_leaf_nodes_key_counter += 1
                    
                
            
            #iterative processing
            nodes_stack.pop()
            children_stack.pop()

    print ("Number of OSHR leaf_nodes is", "{:,}".format(OSHR_leaf_nodes_key_counter))
    print ("Number of OSHR internal nodes is", "{:,}".format(OSHR_internal_nodes_key_counter))
    print ("Total number of reference_leaf_nodes", "{:,}".format(reference_leaf_nodes))
    print ("Total number of reference_internal_nodes", "{:,}".format(reference_internal_nodes))
    print ( "In total of", "{:,}".format(OSHR_leaf_nodes_key_counter + OSHR_internal_nodes_key_counter))
    print ("Cost for indexing reference_internal_nodes and reference_leaf_nodes:", "{:,}".format(cost))

    # --------------------------------------------------------------------------- find base suffixes -------------------------------------------
    
    print ("Finding base suffixes")
    nodes_stack = []
    children_stack = []
    
    nodes_stack.append(tree.root)
    children_stack.append((list(tree.root.transition_links[x] for x in sorted(tree.root.transition_links.keys(), reverse=True))))       
    base_suffix_counter = 0
    
    
    while nodes_stack:
        cost += 1
        current_visited_node = nodes_stack[-1]                  
        if len(children_stack[-1]) > 0:
            last_node_under_top_node_in_stack = children_stack[-1][-1]
            nodes_stack.append(last_node_under_top_node_in_stack)  

            children_stack[-1].pop()                    
            children_stack.append((list(last_node_under_top_node_in_stack.transition_links[x] for x in sorted(last_node_under_top_node_in_stack.transition_links.keys(), reverse=True))))                                          
        else:
            nodes_stack.pop()
            children_stack.pop()

            # alongside processing
            if not current_visited_node.is_leaf():
                #collect base suffixes derived from reference_leaf_node if any
                if hasattr(current_visited_node, "List_of_reference_leaf_nodes"):
                    for reference_leaf_node in current_visited_node.List_of_reference_leaf_nodes:
                        current_visited_node.List_of_base_suffixes.append(reference_leaf_node.idx + 1 + current_visited_node.depth)
                        base_suffix_counter += 1
                        cost += 1
                                                            
                #collect base suffixes derived from reference internal nodes if any
                if hasattr(current_visited_node, "List_of_reference_internal_nodes"):
                    for reference_internal_node in current_visited_node.List_of_reference_internal_nodes:
                        cost += 1
                        for suffix_index_of_leaf_node in tree.List_of_left_to_right_suffix_indexes[reference_internal_node.index_of_leftmost_leaf_in_ST:reference_internal_node.index_of_rightmost_leaf_in_ST + 1]:
                            current_visited_node.List_of_base_suffixes.append(suffix_index_of_leaf_node + 1 + current_visited_node.depth)
                            base_suffix_counter += 1
                            cost += 1
                            

    # compute the case for suffix 0 as there is no previous suffix index for index 0 
    cost += 1
    temp = tree.List_of_leaf_suffix_index_to_leaf_memory[0]                                     
    while temp != tree.root:
        temp = temp.parent
        temp.List_of_base_suffixes.append(0 + temp.depth)
        base_suffix_counter += 1
        cost += 1
            
    # this a special cases and for the root only. The suffix-link of child internal node of a root usually link to the root. In case not, 
    # then the node that the child internal node link to must be bottom-node for the root node.
    cost += 1
    current_visited_node = tree.root
    for node in current_visited_node.transition_links.values():
        cost += 1
        if node.is_leaf():
            if node.idx + 1 < tree.number_leaf_nodes:
                leaf_node_of_next_suffix_index = tree.List_of_leaf_suffix_index_to_leaf_memory[node.idx + 1]
                if leaf_node_of_next_suffix_index.parent == tree.root:
                    current_visited_node.List_of_base_suffixes.append(leaf_node_of_next_suffix_index.idx)
                    base_suffix_counter += 1
        else:
            if node._suffix_link != tree.root:
                for suffix_index_of_leaf_node in tree.List_of_left_to_right_suffix_indexes[node.index_of_leftmost_leaf_in_ST:node.index_of_rightmost_leaf_in_ST + 1]:
                    current_visited_node.List_of_base_suffixes.append(suffix_index_of_leaf_node + 1)
                    base_suffix_counter += 1
                    cost += 1
    
    print ("Total number of base suffixes", "{:,}".format(base_suffix_counter))
    print ("Total time cost:", "{:,}".format(cost))
    

#start = time.time()
#Find_base_suffixes_using_linear_algorithm2(tree)
#print ("Finished in", round((time.time() - start), 5), "seconds")
#print ("------------------------------------------------------------------------------------------")
     
