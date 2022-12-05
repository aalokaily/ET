from suffix_trees import STree
from collections import defaultdict
import time
import math 
from memory_profiler import profile
import sys
import bisect
 
def process_leaf_and_internal_nodes(tree):    
      
    # for iteration process   
    stack = []
    key_stack = []
    children_stack = []
    
    setattr(tree, "temp_internal", defaultdict(int))
    setattr(tree, "temp_leaf", defaultdict(int))
    
    def preprocessing(tree):
        leaf_nodes_key_counter = 0
        tree.leaf_suffix_index_to_leaf_memory_list = [-1] * len(tree.word)
        
        #iterative processing
        stack.append(tree.root)
        key_stack.append(0)
        children_stack.append((list(tree.root.transition_links[x] for x in sorted(tree.root.transition_links.keys(), reverse=True))))
        
        while stack:
            current_node = stack[-1]                  
            if len(children_stack[-1]) > 0:
                last_node_under_top_node_in_stack = children_stack[-1][-1]
                #iterative processing
                stack.append(last_node_under_top_node_in_stack)   # append it to process later with the required order (postorder) and remove it from OSHR[current_node.key]
                key_stack.append(leaf_nodes_key_counter)
                children_stack[-1].pop()                    
                children_stack.append((list(last_node_under_top_node_in_stack.transition_links[x] for x in sorted(last_node_under_top_node_in_stack.transition_links.keys(), reverse=True))))
                                          
            else:
                setattr(current_node, "OT_indexes", [])
                setattr(current_node, "base_suffixes", [])  
                # alongside processing
                if current_node.is_leaf():
                    #tree.temp_leaf[tree._edgeLabel(current_node, tree.root)]
                    # Assigning leaf nodes unique keys
                    tree.number_leaf_nodes += 1                    
                    current_node.key = leaf_nodes_key_counter                     
                    leaf_nodes_key_counter += 1
                    
                    # creating auxiliary lists 
                    tree.leaf_suffix_index_to_leaf_memory_list[current_node.idx] = current_node
                    tree.left_to_right_suffix_indexes_list.append(current_node.idx)
                    
                else:
                    #tree.temp_internal[tree._edgeLabel(current_node, tree.root)]
                    tree.number_internal_nodes += 1
                     
                    # set and assign key_of_leftmost_leaf and key_of_rightmost_leaf attributes to internal nodes
                    setattr(current_node, "key_of_leftmost_leaf", key_stack[-1])
                    setattr(current_node, "key_of_rightmost_leaf", leaf_nodes_key_counter - 1)
                
                                        
                    # construct implicit OSHR tree
                    if current_node._suffix_link is not None and current_node != tree.root:
                        temp = current_node._suffix_link
                        if not hasattr(temp, "nodes_link_to_me"):
                            setattr(temp, "nodes_link_to_me", [])
                        temp.nodes_link_to_me.append(current_node)
                
                    
                #iterative processing 
                stack.pop()
                key_stack.pop()
                children_stack.pop()
                
        print ("Number of internal nodes is", tree.number_internal_nodes)
        print ("Number of leaves is", tree.number_leaf_nodes)
    
    start = time.time()
    preprocessing(tree)
    print ("Processing leaf and internal nodes took", round((time.time() - start), 5), "seconds")
    
    
    #Collect strings under leaf nodes in OSHR tree that needs to compute the key of end node of these strings
    # for iteration process   
    stack = []
    key_stack = []
    children_stack = []
    
def Build_OT_index(tree):

    def phase_1_for_OT_indexing_of_base_paths(tree):
        #index OSHR nodes under ST internal nodes and index inbetween top base nodes
        setattr(tree, "temp", defaultdict(int))
        OSHR_leaf_nodes_key_counter = 0
        OSHR_internal_nodes_key_counter = 0

        #iterative processing
        nodes_stack.append(tree.root)
        OSHR_leaf_nodes_counter_stack.append(0)
        OSHR_internal_nodes_counter_stack.append(0)
        children_stack.append((list(tree.root.transition_links[x] for x in sorted(tree.root.transition_links.keys(), reverse=True))))
        
        while nodes_stack:
            current_node = nodes_stack[-1]                
            if len(children_stack[-1]) > 0:
                last_node_under_top_node_in_stack = children_stack[-1][-1]
                #iterative processing
                nodes_stack.append(last_node_under_top_node_in_stack)     # append it to process later with the required order (postorder) and remove it from OSHR[current_node.key]
                OSHR_leaf_nodes_counter_stack.append(OSHR_leaf_nodes_key_counter)
                OSHR_internal_nodes_counter_stack.append(OSHR_internal_nodes_key_counter)
                children_stack[-1].pop()                    
                children_stack.append((list(last_node_under_top_node_in_stack.transition_links[x] for x in sorted(last_node_under_top_node_in_stack.transition_links.keys(), reverse=True))))
            else:
                # alongside processing
                if not current_node.is_leaf():
                    #find and mark inbetween top base node and assign the reference nodes for this node (which are as coded below)
                    if current_node._suffix_link.parent != current_node.parent._suffix_link:
                        top_node = current_node.parent._suffix_link 
                        bottom_node = current_node._suffix_link
                        
                        n = bottom_node.parent
                        while n  != top_node:
                            if not hasattr(n, "inbetween_top_base_node"):
                                setattr(n, "inbetween_top_base_node", [])
                            n.inbetween_top_base_node.append(current_node)
                            n = n.parent
                    
                    #compute the depth of the deepest non-grand internal node, depth from current_node, under each internal node (non-grand internal node is an internal node where all of its children are leaf nodes)
                    parent_of_current_node = current_node.parent
                    if hasattr(current_node, "depth_of_deepest_non_grand_internal_node"):
                        d = current_node.depth_of_deepest_non_grand_internal_node + current_node.depth
                    else:
                        d = current_node.depth
                                        
                    if hasattr(parent_of_current_node, "depth_of_deepest_non_grand_internal_node"):
                        if d - parent_of_current_node.depth > parent_of_current_node.depth_of_deepest_non_grand_internal_node:
                            parent_of_current_node.depth_of_deepest_non_grand_internal_node = d - parent_of_current_node.depth
                    else:
                        setattr(parent_of_current_node, "depth_of_deepest_non_grand_internal_node", d - parent_of_current_node.depth)

                            
                    # index OSHR leaf and OSHR internal nodes under ST internal nodes    
                    setattr(current_node, "index_of_leftmost_OSHR_leaf", OSHR_leaf_nodes_counter_stack[-1])
                    setattr(current_node, "index_of_rightmost_OSHR_leaf", OSHR_leaf_nodes_key_counter - 1)
                
                    setattr(current_node, "index_of_leftmost_OSHR_internal", OSHR_internal_nodes_counter_stack[-1])
                    setattr(current_node, "index_of_rightmost_OSHR_internal", OSHR_internal_nodes_key_counter - 1)
                        
                    if hasattr(current_node, "nodes_link_to_me"):
                        tree.OSHR_internal_nodes_left_to_right_list.append(current_node)
                        OSHR_internal_nodes_key_counter += 1
                    else:
                        tree.OSHR_leaf_nodes_left_to_right_list.append(current_node)
                        OSHR_leaf_nodes_key_counter += 1
                    
                    
                #iterative processing
                OSHR_leaf_nodes_counter_stack.pop()
                OSHR_internal_nodes_counter_stack.pop()
                nodes_stack.pop()
                children_stack.pop()
    
        print ("Number of OSHR leaf_nodes is", OSHR_leaf_nodes_key_counter)
        print ("Number of OSHR internal nodes is", OSHR_internal_nodes_key_counter)
        print ( "In total of", OSHR_leaf_nodes_key_counter + OSHR_internal_nodes_key_counter)
        
    nodes_stack = []
    OSHR_leaf_nodes_counter_stack = []
    OSHR_internal_nodes_counter_stack = []
    
    children_stack = []
    start = time.time()
    phase_1_for_OT_indexing_of_base_paths(tree)
    print ("\n***** Phase 1 for building OT index for base paths finished in", round((time.time() - start), 5), "seconds")

    def phase_2_for_OT_indexing_of_base_paths(tree):
        #find base paths, record base and bottom nodes, and create OT index
        stack.append(tree.root)
        children_stack.append((list(tree.root.nodes_link_to_me)))
        key_stack.append(-1)
        
        setattr(tree, "temp_dict", defaultdict(list))
            
        while stack:
            current_node = stack[-1]
            #check if OSHR[current_node.key] is empty, then remove it from stack
            if len(children_stack[-1]) > 0:
                last_node_under_top_node_in_stack = children_stack[-1][-1]
                stack.append(last_node_under_top_node_in_stack)     
                children_stack[-1].pop()
                if hasattr(last_node_under_top_node_in_stack, "nodes_link_to_me"):
                    children_stack.append((list(last_node_under_top_node_in_stack.nodes_link_to_me)))
                else:
                    children_stack.append([])
                
                key_stack.append(tree.OT_index_counter)  
                   
            else:
                # collect bottom-base nodes that are OSHR leave nodes
                OSHR_leaf_nodes = []
                if hasattr(current_node, "index_of_leftmost_OSHR_leaf"):
                    OSHR_leaf_nodes = tree.OSHR_leaf_nodes_left_to_right_list[current_node.index_of_leftmost_OSHR_leaf:current_node.index_of_rightmost_OSHR_leaf + 1]
                
                # collect bottom-base nodes collected from reference nodes if current_node is inbetween_top_base_node 
                inbetween_bottom_base_node_dict = defaultdict()  # this dict will be used to distinct nodes under tow difference reference nodes that are linking to the same node under current_node                   
                inbetween_bottom_base_node_list = []
                if hasattr(current_node, "inbetween_top_base_node"):
                    if hasattr(current_node, "nodes_link_to_me"):
                        inbetween_bottom_base_node_dict = defaultdict()  # this dict will be used to distinct nodes under tow difference reference nodes that are linking to the same node under current_node                   
                        for reference_node in  current_node.inbetween_top_base_node:
                            inbetween_bottom_base_node_dict[reference_node._suffix_link] = reference_node._suffix_link
                            if hasattr(reference_node, "index_of_leftmost_OSHR_leaf"):
                                for node in tree.OSHR_leaf_nodes_left_to_right_list[reference_node.index_of_leftmost_OSHR_leaf:reference_node.index_of_rightmost_OSHR_leaf + 1]:
                                    inbetween_bottom_base_node_dict[node._suffix_link] = node._suffix_link
                            if hasattr(reference_node, "index_of_leftmost_OSHR_internal"):
                                for node in  tree.OSHR_internal_nodes_left_to_right_list[reference_node.index_of_leftmost_OSHR_internal:reference_node.index_of_rightmost_OSHR_internal + 1]:
                                    inbetween_bottom_base_node_dict[node._suffix_link] = node._suffix_link
                    else:
                        if hasattr(current_node, "index_of_leftmost_OSHR_internal"):
                            inbetween_bottom_base_node_list  = tree.OSHR_internal_nodes_left_to_right_list[current_node.index_of_leftmost_OSHR_internal:current_node.index_of_rightmost_OSHR_internal + 1]
                    
                # the following 6 lines cover a special case and for the root only. The suffix-link of child internal node of a root usually link to the root. In case not, 
                # then the node that the child internal node link to must be bottom-node for the root node.
                root_bottom_nodes = []
                if current_node == tree.root:
                    for node in current_node.transition_links.values():
                        if not node.is_leaf():
                            if node._suffix_link != tree.root:
                                root_bottom_nodes.append(node._suffix_link)


                for bottom_base_node in list(inbetween_bottom_base_node_dict.values()) + OSHR_leaf_nodes + inbetween_bottom_base_node_list + root_bottom_nodes:
                    mapping_guided_suffix = tree.left_to_right_suffix_indexes_list[bottom_base_node.key_of_leftmost_leaf]
                    suffix_starting_from_current_node = mapping_guided_suffix + current_node.depth
                    if suffix_starting_from_current_node < tree.number_leaf_nodes:
                        index_key_of_suffix_starting_from_current_node_in_ST = tree.leaf_suffix_index_to_leaf_memory_list[suffix_starting_from_current_node].key
                                        
                        if bottom_base_node.depth - current_node.depth not in tree.temp_dict:
                            tree.temp_dict[bottom_base_node.depth - current_node.depth] = []                                    
                        tree.temp_dict[bottom_base_node.depth - current_node.depth].append((index_key_of_suffix_starting_from_current_node_in_ST, tree.OT_index_counter))
                        tree.OT_index[tree.OT_index_counter] = mapping_guided_suffix + current_node.depth
                        tree.OT_index_counter += 1
                    
                    
                if not hasattr(current_node, "left_OT_index"):
                    setattr(current_node, "left_OT_index", int)
                    setattr(current_node, "right_OT_index", int)
                    
                current_node.left_OT_index = key_stack[-1]
                current_node.right_OT_index = tree.OT_index_counter 
                
                    
                key_stack.pop()
                stack.pop()
                children_stack.pop()
        
        for key in sorted(tree.temp_dict):
            tt = sorted(tree.temp_dict[key])
            tree.temp_dict[key] = list(reversed(tt))        
            
        print ("Length of OT index ", tree.OT_index_counter)
        print ("Left and right OT index of root",  tree.root.left_OT_index + 1, tree.root.right_OT_index)
        
        
    stack = []
    children_stack = []
    key_stack = []
    tree.OT_index_counter = 0

        
    start = time.time()
    phase_2_for_OT_indexing_of_base_paths(tree)
    print ("\n***** Phase 2 for building OT index for base paths finished in", round((time.time() - start), 5), "seconds")
    
    
    def phase_3_for_OT_indexing_of_base_paths(tree):
        #map OT indexes of base paths to same path starting from root of ST, then sort OT indexes
        #iterative processing
        nodes_stack.append(tree.root)
        children_stack.append((list(tree.root.transition_links[x] for x in sorted(tree.root.transition_links.keys(), reverse=True))))
        
        temp = defaultdict(int)
        sum_of_all_OT_indexes = 0
        
        while nodes_stack:
            current_node = nodes_stack[-1]                
            if len(children_stack[-1]) > 0:
                last_node_under_top_node_in_stack = children_stack[-1][-1]
                #iterative processing
                nodes_stack.append(last_node_under_top_node_in_stack)     # append it to process later with the required order (postorder) and remove it from OSHR[current_node.key]
                children_stack[-1].pop()                    
                children_stack.append((list(last_node_under_top_node_in_stack.transition_links[x] for x in sorted(last_node_under_top_node_in_stack.transition_links.keys(), reverse=True))))
            else:
                # alongside processing
                if not current_node.is_leaf():
                    setattr(current_node, "OT_indexes", [])
                    if current_node.depth in tree.temp_dict:
                        #print (tree.temp_dict[current_node.depth])
                        for i in range(len(tree.temp_dict[current_node.depth])-1, -1, -1):
                            temp = tree.temp_dict[current_node.depth]
                            key_of_suffix_idx = temp[i][0]
                            OT_index = temp[i][1]
                        
                            if current_node.key_of_leftmost_leaf <= key_of_suffix_idx <= current_node.key_of_rightmost_leaf:
                                current_node.OT_indexes.append(OT_index)
                                tree.temp_dict[current_node.depth].pop()
                            else:
                                break
                                
                    # now sort OT indexes for each transition letters
                    current_node.OT_indexes.sort()
                    sum_of_all_OT_indexes += len(current_node.OT_indexes)
                    #print (len(current_node.OT_indexes), current_node.key_of_rightmost_leaf - current_node.key_of_leftmost_leaf)
                    
                #iterative processing 
                nodes_stack.pop()
                children_stack.pop()
    
        print ("sum_of_all_OT_indexes", sum_of_all_OT_indexes)
            
    nodes_stack = []
    children_stack = []
    start = time.time()
    phase_3_for_OT_indexing_of_base_paths(tree)
    print ("\n***** Phase 3 for building OT index for base paths finished in", round((time.time() - start), 5), "seconds")  

    
   
######################################################################################## Searching code ##############################################################################################################

def find_approximate_matching(tree, sentinel_character, given_pattern_length, pattern, k_value_to_search_for, last_number_of_mismatches, main_node, suffixes_traversals):
    # path_of_nodes_for_pattern contains the path of the pattern in ST
    # suffixes_traversals contains m elements where element at position i contain a tuple of (end_node, k, errors_positions) where end_node is the end node of the path of the ith suffix of the pattern in ST
    # k is the number of mismatches encountered on edges, and errors_positions is the position of mismatch found in the path. 
    
    complete_matching_results = defaultdict(list)
    incomplete_matching_results = defaultdict(list)
    
    pattern_length = len(pattern)
    depth_of_main_node = main_node.depth
    depth_in_tree_to_search_for = pattern_length + depth_of_main_node
    
    #print ("---------- calling " + tree._edgeLabel(main_node, tree.root)[:50], k_value_to_search_for, last_number_of_mismatches, pattern, depth_of_main_node)
    
    if pattern_length == 0:   # means depth of main_node is now larger than the length of given pattern (original pattern) so collect results
        complete_matching_results[last_number_of_mismatches].append((main_node, []))
        #print ("completed_results when pattern_length is zero", tree._edgeLabel(main_node, tree.root)[:30])
    
    else:
        branching_letters_and_nodes = compute_distance_with_edges_of_child_nodes_under_a_node(tree, sentinel_character, pattern, k_value_to_search_for, main_node, suffixes_traversals)
        for info in branching_letters_and_nodes:
            transition_node = info[0]
            number_of_mismatches = info[1]
            mismatches_positions = info[2]
            
            #print ("transition_matching", tree._edgeLabel(transition_node, main_node)[:50], number_of_mismatches, mismatches_positions, transition_node.is_leaf())
                
            if transition_node.depth >= depth_in_tree_to_search_for:
                if number_of_mismatches == k_value_to_search_for:
                    complete_matching_results[last_number_of_mismatches + number_of_mismatches].append((transition_node, mismatches_positions))
                    #print ("completed_results using transition internal node", tree._edgeLabel(transition_node, tree.root)[:30])
                elif  0 <= number_of_mismatches < k_value_to_search_for + last_number_of_mismatches:
                    complete_matching_results[last_number_of_mismatches + number_of_mismatches].append((transition_node, mismatches_positions)) 
                    #print ("completed_results of < given_k using transition internal node", tree._edgeLabel(transition_node, tree.root)[:30])
            
            elif 0 <= number_of_mismatches <= k_value_to_search_for and transition_node.depth - depth_of_main_node < pattern_length:
                d = transition_node.depth - depth_of_main_node
                suffix_end_node = suffixes_traversals[d][-1]
                
                #print ("OT index", tree._edgeLabel(transition_node, tree.root), tree._edgeLabel(suffix_end_node, tree.root)[:30], suffix_end_node.depth, number_of_mismatches , k_value_to_search_for)
                if number_of_mismatches < k_value_to_search_for:
                    incomplete_matching_results[last_number_of_mismatches + number_of_mismatches].append((transition_node, mismatches_positions))
                    #print ("incompleted_results when number_of_mismatches < k_value_to_search_for", tree._edgeLabel(transition_node, tree.root)[:30])
                
                elif suffix_end_node.depth >= depth_in_tree_to_search_for - transition_node.depth: # and number_of_mismatches must == k_value_to_search_for
                    # check first if matching results is within the direct child nodes under transition_node
                    did_not_find_matching_under_transition_node = True
                    for node in transition_node.transition_links.values():
                        if node.depth >= depth_in_tree_to_search_for:
                            if node.is_leaf():
                                suffix_number_under_node = tree.leaf_suffix_index_to_leaf_memory_list[node.idx + transition_node.depth]
                                if suffix_end_node.is_leaf():
                                    if suffix_number_under_node.key == suffix_end_node.key:
                                        complete_matching_results[last_number_of_mismatches + number_of_mismatches].append((node, mismatches_positions))
                                        did_not_find_matching_under_transition_node = False
                                        #print ("completed_results when suffix_end_node is leaf node under transition_node and suffix_end_node is leaf", tree._edgeLabel(node, tree.root)[:30])
                                else:
                                    if suffix_number_under_node.key  >= suffix_end_node.key_of_leftmost_leaf and suffix_number_under_node.key <= suffix_end_node.key_of_rightmost_leaf:
                                        complete_matching_results[last_number_of_mismatches + number_of_mismatches].append((node, mismatches_positions))
                                        did_not_find_matching_under_transition_node = False
                                        #print ("completed_results when suffix_end_node is leaf node under transition_node and suffix_end_node is internal", tree._edgeLabel(node, tree.root)[:30])
                            else:
                                tt = tree.left_to_right_suffix_indexes_list[node.key_of_leftmost_leaf]
                                any_suffix_under_transition_node = tree.leaf_suffix_index_to_leaf_memory_list[tt + transition_node.depth]
                                
                                if suffix_end_node.is_leaf():
                                    if any_suffix_under_transition_node.key == suffix_end_node.key:
                                        complete_matching_results[last_number_of_mismatches + number_of_mismatches].append((node, mismatches_positions))
                                        did_not_find_matching_under_transition_node = False
                                        #print ("completed_results when suffix_end_node is internal node under transition_node and suffix_end_node is leaf", tree._edgeLabel(node, tree.root)[:30])
                                else:
                                    if any_suffix_under_transition_node.key  >= suffix_end_node.key_of_leftmost_leaf and any_suffix_under_transition_node.key <= suffix_end_node.key_of_rightmost_leaf:
                                        complete_matching_results[last_number_of_mismatches + number_of_mismatches].append((node, mismatches_positions))
                                        did_not_find_matching_under_transition_node = False
                                        #print ("completed_results when suffix_end_node is internal node under transition_node and suffix_end_node is internal", tree._edgeLabel(node, tree.root)[:30])
                            
                    if did_not_find_matching_under_transition_node:
                        ll = transition_node.depth - depth_of_main_node
                        chrt = pattern[ll]
                        if chrt in transition_node.transition_links:
                            ttt = transition_node.transition_links[chrt]
                            if not ttt.is_leaf():
                                min_depth = ttt.depth - transition_node.depth
                                if hasattr (ttt, "depth_of_deepest_non_grand_internal_node"): # this also to make sure that there are descandant internal node
                                    max_depth = min_depth + ttt.depth_of_deepest_non_grand_internal_node
                                else:
                                    max_depth = min_depth
                                    
                                try:
                                    suffix_end_node = suffixes_traversals[d][max_depth]
                                except:
                                    suffix_end_node = suffixes_traversals[d][-1]
                                
                                while suffix_end_node.depth >= min_depth:
                                    left_position  =  bisect.bisect_left(suffix_end_node.OT_indexes, transition_node.left_OT_index)
                                    right_position =  bisect.bisect_left(suffix_end_node.OT_indexes, transition_node.right_OT_index)
                                    if left_position != right_position:
                                        #print ("Found using OT index")
                                        OT_index_of_a_base_path = suffix_end_node.OT_indexes[left_position]
                                        guided_suffix = tree.OT_index[OT_index_of_a_base_path]
                                        suffix_to_search_for = guided_suffix - transition_node.depth
                                        key_of_suffix_to_search_for = tree.leaf_suffix_index_to_leaf_memory_list[suffix_to_search_for].key
                                        depth_required = suffix_end_node.depth 
                                        matching_node = find_end_node_given_suffix_key_and_depth(transition_node, key_of_suffix_to_search_for, depth_required)
                                        #print (matching_node.depth , depth_in_tree_to_search_for, tree._edgeLabel(matching_node, tree.root)[:30])
                                        if matching_node.depth >= depth_in_tree_to_search_for:
                                            complete_matching_results[last_number_of_mismatches + number_of_mismatches].append((matching_node, mismatches_positions))
                                            #print ("completed_results using OT index", tree._edgeLabel(matching_node, tree.root)[:30])
                                        else:
                                            d = matching_node.depth - depth_of_main_node
                                            suffix_end_node = suffixes_traversals[d][-1]
                                            
                                            for node in matching_node.transition_links.values():
                                                #print (tree._edgeLabel(node, tree.root)[:30])
                                                if node.depth >= depth_in_tree_to_search_for:
                                                    if node.is_leaf():
                                                        suffix_number_under_node = tree.leaf_suffix_index_to_leaf_memory_list[node.idx + matching_node.depth]
                                                        if suffix_end_node.is_leaf():
                                                            if suffix_number_under_node.key == suffix_end_node.key:
                                                                complete_matching_results[last_number_of_mismatches + number_of_mismatches].append((node, mismatches_positions))
                                                        else:
                                                            if suffix_number_under_node.key  >= suffix_end_node.key_of_leftmost_leaf and suffix_number_under_node.key <= suffix_end_node.key_of_rightmost_leaf:
                                                                complete_matching_results[last_number_of_mismatches + number_of_mismatches].append((node, mismatches_positions))
                                                                
                                                    else:
                                                        tt = tree.left_to_right_suffix_indexes_list[node.key_of_leftmost_leaf]
                                                        any_suffix_under_matching_node = tree.leaf_suffix_index_to_leaf_memory_list[tt + matching_node.depth]
                                                        
                                                        if suffix_end_node.is_leaf():
                                                            if any_suffix_under_matching_node.key == suffix_end_node.key:
                                                                complete_matching_results[last_number_of_mismatches + number_of_mismatches].append((node, mismatches_positions))
                                                        else:
                                                            if any_suffix_under_matching_node.key  >= suffix_end_node.key_of_leftmost_leaf and any_suffix_under_matching_node.key <= suffix_end_node.key_of_rightmost_leaf:
                                                                complete_matching_results[last_number_of_mismatches + number_of_mismatches].append((node, mismatches_positions))
                                        break
                                    else:
                                        suffix_end_node = suffix_end_node.parent
                                        #print ("backtracking", tree._edgeLabel(suffix_end_node, tree.root)[:30])
                                     



    return (complete_matching_results, incomplete_matching_results)
   

  
def compute_distance_with_edges_of_child_nodes_under_a_node(tree, sentinel_character, pattern, k_value_to_search_for, main_node, suffixes_traversals):
    
    results = []
    
    pattern_length = len(pattern)
    depth_of_main_node = main_node.depth
    depth_in_tree_to_search_for = pattern_length + depth_of_main_node
    
    if k_value_to_search_for == 0:
        if pattern[0] in main_node.transition_links:
            transition_node = main_node.transition_links[pattern[0]]
            if transition_node not in tree.incomplete_nodes_found_using_OT_index:
                if transition_node.depth - depth_of_main_node == 1:
                    results.append((transition_node, 0, []))
                else:
                    end_node_of_suffix_starting_from_root = suffixes_traversals[0][-1]
                    if end_node_of_suffix_starting_from_root.depth >= pattern_length:
                        if transition_node.is_leaf():
                            suffix_number_under_node = tree.leaf_suffix_index_to_leaf_memory_list[transition_node.idx + depth_of_main_node]
                            if end_node_of_suffix_starting_from_root.is_leaf():
                                if suffix_number_under_node.key == end_node_of_suffix_starting_from_root.key:
                                    results.append((transition_node, 0, []))
                            else:
                                if suffix_number_under_node.key  >= end_node_of_suffix_starting_from_root.key_of_leftmost_leaf and suffix_number_under_node.key <= end_node_of_suffix_starting_from_root.key_of_rightmost_leaf:
                                    results.append((transition_node, 0, []))
                        else:
                            l = transition_node.idx + depth_of_main_node
                            if transition_node.depth >= depth_in_tree_to_search_for:
                                d = depth_in_tree_to_search_for - depth_of_main_node
                            else:
                                d = transition_node.depth  - depth_of_main_node
                            end_node_of_suffix_starting_from_root = suffixes_traversals[0][d]
                            tt = tree.left_to_right_suffix_indexes_list[transition_node.key_of_leftmost_leaf]
                            any_suffix_under_transition_node = tree.leaf_suffix_index_to_leaf_memory_list[tt + depth_of_main_node]
                            
                            if end_node_of_suffix_starting_from_root.is_leaf():
                                if any_suffix_under_transition_node.key == end_node_of_suffix_starting_from_root.key:
                                    results.append((transition_node, 0, []))
                            else:
                                if end_node_of_suffix_starting_from_root != tree.root:
                                    if any_suffix_under_transition_node.key  >= end_node_of_suffix_starting_from_root.key_of_leftmost_leaf and any_suffix_under_transition_node.key <= end_node_of_suffix_starting_from_root.key_of_rightmost_leaf:
                                        results.append((transition_node, 0, []))
                                    
    
    elif k_value_to_search_for > 0:
        for transition_letter in main_node.transition_links.keys():
            transition_node = main_node.transition_links[transition_letter]
            if transition_node not in tree.incomplete_nodes_found_using_OT_index:
                if transition_node.depth - depth_of_main_node == 1:
                    if transition_letter != sentinel_character:
                        if transition_letter == pattern[0]:
                            results.append((transition_node, 0, []))
                        else:
                            results.append((transition_node, 1, [0]))
                else:
                    if transition_node.is_leaf():
                        if transition_node.depth >= depth_in_tree_to_search_for:
                            if k_value_to_search_for > pattern_length:
                                k_value_to_search_for = pattern_length
                            temp = Hamming_distance(tree.word[transition_node.idx + depth_of_main_node:transition_node.idx + depth_of_main_node + k_value_to_search_for], pattern[:k_value_to_search_for])
                            if temp != [-1]:
                                mismatches = 0
                                mismatches_positions = []
                                for i, j in enumerate(temp):
                                    if j == 1:
                                        mismatches += 1 
                                        mismatches_positions.append(i )
                                        if mismatches > k_value_to_search_for:
                                            break
                                
                                if k_value_to_search_for == pattern_length: 
                                    if mismatches <= k_value_to_search_for:
                                        results.append((transition_node, mismatches, mismatches_positions))
                                else:
                                    suffix_end_node = suffixes_traversals[k_value_to_search_for][-1]
                                    
                                    if mismatches == k_value_to_search_for:
                                        any_suffix_under_transition_node = tree.leaf_suffix_index_to_leaf_memory_list[transition_node.idx + depth_of_main_node + k_value_to_search_for]
                                        if suffix_end_node.is_leaf():
                                            if any_suffix_under_transition_node.key == suffix_end_node.key:
                                                results.append((transition_node, mismatches, mismatches_positions))
                                        else:
                                            if suffix_end_node.depth >= pattern_length - k_value_to_search_for:
                                                if any_suffix_under_transition_node.key  >= suffix_end_node.key_of_leftmost_leaf and any_suffix_under_transition_node.key <= suffix_end_node.key_of_rightmost_leaf:
                                                    results.append((transition_node, mismatches, mismatches_positions))
                                    
                                    else:
                                        f = True
                                        key_of_leaf_node = tree.leaf_suffix_index_to_leaf_memory_list[transition_node.idx + depth_of_main_node + k_value_to_search_for].key # key_of_leaf_node with idx starting from root equal to transition_idx under current node
                                        while f:
                                            if suffix_end_node.is_leaf():
                                                if key_of_leaf_node == suffix_end_node.key:
                                                    f = False
                                                    results.append((transition_node, mismatches, mismatches_positions))
                                                else:
                                                    suffix_end_node = suffix_end_node.parent
                                            else:
                                                if key_of_leaf_node  >= suffix_end_node.key_of_leftmost_leaf and key_of_leaf_node <= suffix_end_node.key_of_rightmost_leaf:
                                                    f = False
                                                    l = transition_node.idx + depth_of_main_node + k_value_to_search_for
                                                    temp = Hamming_distance(tree.word[l:l + pattern_length - k_value_to_search_for], pattern[k_value_to_search_for:])
                                                    if temp != [-1]:
                                                        for i, j in enumerate(temp):
                                                            if j == 1:
                                                                mismatches += 1 
                                                                mismatches_positions.append(i + k_value_to_search_for + suffix_end_node.depth)
                                                                if mismatches > k_value_to_search_for:
                                                                    break
                                                    
                                                        if mismatches <= k_value_to_search_for:
                                                            results.append((transition_node, mismatches, mismatches_positions))
                                                        
                                                else:
                                                    suffix_end_node = suffix_end_node.parent
                                                    
                                
                    else:
                        l = transition_node.idx + depth_of_main_node
                        if transition_node.depth >= depth_in_tree_to_search_for:
                            d = depth_in_tree_to_search_for - depth_of_main_node
                        else:
                            d = transition_node.depth  - depth_of_main_node
                        
                        temp = Hamming_distance(tree.word[l:l + d], pattern[:d])
                        if temp != [-1]:
                            mismatches = 0
                            mismatches_positions = []
                            for i, j in enumerate(temp):
                                if j == 1:
                                    mismatches += 1 
                                    mismatches_positions.append(i)
                                    if mismatches > k_value_to_search_for:
                                        break
                                
                            if mismatches <= k_value_to_search_for:
                                results.append((transition_node, mismatches, mismatches_positions))
                    
    return results
    
########################################################## Function for OT index ###############################################    
   
def find_end_node_of_exact_path_of_string_starting_from_a_node(tree, string, node, suffixes_traversals):          
    current_node = node
    i = 0
    l = len(string)
    d = node.depth
    f = True
    mismatch_in_middle_of_edge = False
    end_node = node
    while f:
        if i <= l - 1:
            if string[i] in current_node.transition_links:
                end_node = current_node.transition_links[string[i]]
                if end_node.is_leaf():
                    d2 = current_node.depth - d 
                    suffix_end_node = suffixes_traversals[d2][-1]
                    suffix_number_under_node = tree.leaf_suffix_index_to_leaf_memory_list[end_node.idx + current_node.depth]
                    if suffix_end_node.is_leaf():
                        if suffix_number_under_node.key == suffix_end_node.key:
                            return end_node
                        else:
                            return end_node.parent
                    else:
                        if suffix_number_under_node.key  >= suffix_end_node.key_of_leftmost_leaf and suffix_number_under_node.key <= suffix_end_node.key_of_rightmost_leaf:
                            return end_node
                        else:
                            return end_node.parent

                else:
                    if end_node.depth >= l + d:
                        edge_label = tree.word[end_node.idx + current_node.depth:end_node.idx + l + d]
                    else:
                        edge_label = tree.word[end_node.idx + current_node.depth:end_node.idx + end_node.depth]
                    
                    current_node = end_node
                    for char in edge_label:
                        if string[i] == char:
                            i += 1
                        else:
                            f = False
                            mismatch_in_middle_of_edge = True
                            break
            else:
                f = False
                break
        else:
            f = False
            break
            
    if end_node.depth - current_node.depth > l:       
        return end_node.parent
    elif end_node.depth - current_node.depth == l:
        return end_node
    else:
        if mismatch_in_middle_of_edge:
            return "N"
        else:
            return end_node
     

def find_end_node_given_suffix_key_and_depth(node, suffix_key, required_depth):
    
    depth_of_starting_node = node.depth
    end_node = None
    
    if not isinstance(required_depth, int) or required_depth < 0:
        return end_node
    
    f = True
    while f:
        for child_node in node.transition_links.values():
            if child_node.is_leaf():
                if child_node.key == suffix_key:
                    if child_node.depth - depth_of_starting_node >= required_depth:
                        end_node = child_node
                        f = False
            else:
                if child_node.key_of_leftmost_leaf <= suffix_key <= child_node.key_of_rightmost_leaf:
                    if child_node.depth - depth_of_starting_node >= required_depth:
                        end_node = child_node
                        f = False
                    else:
                        node = child_node
                            
    return end_node
    
########################################################## Functions for Finding end nodes of suffixes in pattern  ###############################################

def find_end_node_of_each_suffix_of_pattern(tree, pattern):
    suffixes_traversals = []
    # compute suffixes paths of nodes
    pattern_length = len(pattern)
    
    end_node = find_end_node_of_exact_match(tree, pattern, tree.root)
    suffixes_traversals.append(end_node)

    for i in range(1, pattern_length):
        end_node_of_last_suffix = suffixes_traversals[-1]
        
        if end_node_of_last_suffix.is_leaf():
            node = end_node_of_last_suffix.parent._suffix_link
            end_node = find_end_node_of_exact_match(tree, pattern[i + node.depth:], node)

        else:
            if end_node_of_last_suffix.depth <= pattern_length - i + 1:
                node = end_node_of_last_suffix._suffix_link
            else:
                node = end_node_of_last_suffix.parent._suffix_link
                
            end_node = find_end_node_of_exact_match(tree, pattern[i + node.depth:], node)
                
        suffixes_traversals.append(end_node)
        
        #print (i, tree._edgeLabel(node, tree.root)[:100], pattern[i + node.depth:], tree._edgeLabel(end_node, tree.root)[:100])
        #print (find_all_nodes_in_path_of_string_starting_from_a_node(pattern[i:], tree.root))
    
    return suffixes_traversals
    
def find_end_node_of_exact_match(tree, string, starting_node):          
    current_node = starting_node
    i = 0
    l = len(string)
    d = starting_node.depth
    f = True
    mismatch_in_middle_of_edge = False
    end_node = starting_node
    while f:
        if i <= l - 1:
            if string[i] in current_node.transition_links:
                end_node = current_node.transition_links[string[i]]
                if end_node.depth >= d + l:
                    edge_label = tree.word[end_node.idx + current_node.depth:end_node.idx + l + d]
                else:
                    edge_label = tree.word[end_node.idx + current_node.depth:end_node.idx + end_node.depth]
                
                current_node = end_node
                for char in edge_label:
                    if string[i] == char:
                        i += 1
                    else:
                        f = False
                        break
            else:
                f = False
                break
        else:
            f = False
            break
            
    
    if i == l:
        return end_node
    else:#i must be then less than l
        if end_node.depth - starting_node.depth == i:     
            return end_node
        else:
            return end_node.parent
            
    
######################################################## Auxillary functions ################################################################################

def Hamming_distance(s1,s2):
    if len(s1)!=len(s2):
        return [-1]
    else:
        p = []
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                p.append(1)
            else:
                p.append(0)
    return p        


def print_results_given_list_of_node(tree, matching_nodes, pattern, pattern_length, k):
    #output _results
    
    print ("------------------------------------------------------------------------")
    print ("Approximate matching for k value of ", k)
    print ("------------------------------------------------------------------------")
    if matching_nodes:
        tt = defaultdict(int)   # to hash approximate matching i order to check if the outcomes has duplicates. If the approximate matching is correct, no duplicates should be presented in the approximate matching. 
        position_combinations = defaultdict(int)
        i = 0
        different_distance = False
        different_positions = False
        matching_nodes.sort(key=lambda x: x[1])
        
        for it in matching_nodes:
            matching_node = it[0]
            positions = it[1]
            
            if matching_node.is_leaf():
                print (tree.word[matching_node.idx :matching_node.idx + pattern_length], sum(Hamming_distance(tree.word[matching_node.idx :matching_node.idx + pattern_length], pattern)),  positions, matching_node.idx, "leaf node")
                i += 1
                tt[matching_node.idx] += 1
                position_combinations["-".join([str(x) for x in positions])] = 0
                if k != sum(Hamming_distance(tree.word[matching_node.idx :matching_node.idx + pattern_length], pattern)):
                    different_distance = True
                if k != len (positions):
                    different_positions = True
            else:
                for suffix_index in tree.left_to_right_suffix_indexes_list[matching_node.key_of_leftmost_leaf:matching_node.key_of_rightmost_leaf +1]: 
                    print (tree.word[suffix_index :suffix_index + pattern_length], sum(Hamming_distance(tree.word[suffix_index :suffix_index + pattern_length], pattern)), positions, suffix_index)
                    i += 1
                    tt[suffix_index] += 1
                    position_combinations["-".join([str(x) for x in positions])] = 0
                    if k != sum(Hamming_distance(tree.word[suffix_index :suffix_index + pattern_length], pattern)):
                        different_distance = True
                    if k != len (positions):
                        different_positions = True

        if len(tt) != i:
            print ("ALERT: duplicates is presented in the approximate matching", len(tt), i)
            for kk in tt:
                if tt[kk] > 1:
                    print ("duplicate at position", kk)
        else:
            print ("\nNumber of matching is", len(tt))
            #print ("No duplicates (results with same index in the reference text) is presented in the approximate matching")
            print ("Number of position_combinations in the results", len(position_combinations))
            print ("Number of expected combinations", int(math.factorial(pattern_length)/(math.factorial(pattern_length-k) * math.factorial(k))))
            
        if i > 0: # means there was a result
            if different_distance:
                print ("There are matching_results with distance different than", k)
            else:
                print ("All matching_results is with a distance equal to", k, "as should be")
                
            if different_positions:
                print ("There are mismatches positions different than", k)
            else:
                print ("All mismatches positions is equal to", k, "as should be")
    else:
        print ("No approximate matching found")
     
#################################################### Search for query functions ##############################################################  


def find_all_nodes_in_path_of_string_starting_from_a_node(tree, string, starting_node):          
    current_node = starting_node
    errors_positions = []
    k = 0
    all_nodes = [[current_node, k, list(errors_positions)]]
    
    i = 0
    l = len(string)        
    f = True        
    while f:
        if string[i] in current_node.transition_links:
            end_node = current_node.transition_links[string[i]]
            if end_node.is_leaf():
                edge_label = tree.word[end_node.idx + current_node.depth:end_node.idx + current_node.depth + l]
            else:
                edge_label = tree.word[end_node.idx + current_node.depth:end_node.idx + end_node.depth]
            
            for char in edge_label:
                if i < l: 
                    if string[i] != char:
                        k += 1
                        errors_positions.append(i)
                    i += 1
                else:
                    all_nodes.append([end_node, k, list(errors_positions)])
                    f = False
                    break
            if f:
                all_nodes.append([end_node, k, list(errors_positions)])
                current_node = end_node
            if i == l:
                f = False
        else:               
            f = False
    
    return all_nodes



def start():
    start_er = time.time()
    
    start = time.time()
    
    input_file = sys.argv[1]    
    given_k = int(sys.argv[2])
    pattern = sys.argv[3]
    pattern_length = len(pattern)
    print ("Length of pattern", pattern_length)
    
    if given_k <= 0  or given_k > pattern_length:
        print ("Please choose K value to be greater than 0 and greater than or equal to length of the pattern")
    
    else:
        text = ""
        with open(input_file) as file_in:        
            for line in file_in:
                if line[0] != ">":
                    text += line.strip()
                    
        #text += "$" # the implementation of suffix tree adds a sentinel character so no need to do this.  
        
        print ("Reading input data took", round((time.time() - start), 5), "seconds")   
        
        print ("------------------------------------------------------------------------------------------")
        start = time.time()     
        tree = STree.STree(text)
        sentinel_character  = tree.word[-1]
        print ("Building Suffix Tree took", round((time.time() - start), 5), "seconds")
        
        start = time.time()
        # set tree attributes
        setattr(tree, "OT_index_counter", 0)
        setattr(tree, "number_leaf_nodes", 0)
        setattr(tree, "number_internal_nodes", 0)
        setattr(tree, "left_to_right_suffix_indexes_list", [])
        setattr(tree, "leaf_suffix_index_to_leaf_memory_list", [])
        setattr(tree, "OSHR_leaf_nodes_left_to_right_list", []) 
        setattr(tree, "OSHR_internal_nodes_left_to_right_list", []) 
        setattr(tree, "OT_index", defaultdict())
        
        print ("------------------------------------------------------------------------------------------")
        process_leaf_and_internal_nodes(tree)
        
        print ("------------------------------------------------------------------------------------------")    
        start = time.time()
        Build_OT_index(tree)
        print ("Building OT index using base paths took", round((time.time() - start), 5), "seconds")
        
        tree.word = tree.word[:-1]# this will removed the added sentinel_character from the text (word) so that it will not be included in the comparison and results finding
        
        pattern_length = len(pattern)
        start = time.time()
        starting_node = tree.root
        depth_in_tree_to_search_for = pattern_length + starting_node.depth
        path_of_nodes_for_pattern_from_starting_node = find_all_nodes_in_path_of_string_starting_from_a_node(tree, pattern, starting_node)
        suffixes_traversals = []
        i = pattern_length
        temp = find_end_node_of_each_suffix_of_pattern(tree, pattern)
        for end_node in temp:
            i -= 1
            t = []  
            
            while end_node != tree.root:
                t.append(end_node)
                end_node = end_node.parent
            t = [tree.root] + t[::-1] 

            res = [tree.root]
            for j in range(len(t)-1):
                for d in range(t[j+1].depth - t[j].depth):
                    if d + t[j].depth <= i:
                        res.append(t[j+1])
            
            suffixes_traversals.append(res)

        
        
        tree.incomplete_nodes_found_using_OT_index = defaultdict(int)
        tree.complete_matching_results = defaultdict(int)
        tree.incomplete_matching_results = defaultdict(int)   # this dict to handle the incomplete matching that caused by no transition state (the pattern for instance has a character that is not within the alphabet of the input data)
        
        for info in path_of_nodes_for_pattern_from_starting_node:
            end_node = info[0]
            num_mismatches = info[1]
            mismatches_positions = info[2]
            if not end_node.is_leaf():
                if num_mismatches  < given_k:
                    if num_mismatches not in tree.incomplete_matching_results:
                        tree.incomplete_matching_results[num_mismatches] = []
                    tree.incomplete_matching_results[num_mismatches].append((end_node, mismatches_positions))
                    tree.incomplete_nodes_found_using_OT_index[end_node] = 0
        
        while True:
            a = sorted(list(tree.incomplete_matching_results.keys()))
            if len(a) == 0:
                break
            elif a[0] > given_k:
                break
                
            temp = tree.incomplete_matching_results.copy()
            tree.incomplete_matching_results.clear()
            for key in temp.keys():
                for ele in temp[key]:
                    searching_node = ele[0]
                    mismatches_pos_from_before = ele[1]
                    
                    k_value_to_search_for = given_k - key
                    last_num_of_mismatches = key
                    tt = find_approximate_matching(tree, sentinel_character, pattern_length, pattern[searching_node.depth - starting_node.depth:], k_value_to_search_for, last_num_of_mismatches, searching_node, suffixes_traversals[searching_node.depth - starting_node.depth:])
                    
                    for k2 in tt[0].keys():   # tt[0] is the returned dictionary of find_approximate_matching function that contains the complete matching results of the given k or less
                        if k2 not in tree.complete_matching_results:
                            tree.complete_matching_results[k2] = []
                            
                        for elem in tt[0][k2]:
                            end_node = elem[0]
                            mismatches_pos = elem[1]
                        
                            tree.complete_matching_results[k2].append((end_node, mismatches_pos_from_before + [x + searching_node.depth - starting_node.depth for x in mismatches_pos]))
                        
                    for k2 in tt[1].keys(): # tt[1] is the returned dictionary of find_approximate_matching function that contains the incomplete/partial matching with the pattern
                        if k2 not in tree.incomplete_matching_results:
                            tree.incomplete_matching_results[k2] = []
                            
                        for ele in tt[1][k2]:
                            node = ele[0]
                            mismatches_pos = ele[1]
                            
                            tree.incomplete_matching_results[k2].append((node, mismatches_pos_from_before + [x + searching_node.depth - starting_node.depth for x in mismatches_pos]))
                            
                            
        end_time = time.time()
        
        for k in range(1, given_k + 1):
            print_results_given_list_of_node(tree, tree.complete_matching_results[k] , tree._edgeLabel(starting_node, tree.root) + pattern, depth_in_tree_to_search_for, k) 
        

        print ("Found approximate matching for", pattern, "when 1 <= k <=", given_k, "in ", round((end_time - start), 5), "seconds")
    
        tree.incomplete_nodes_found_using_OT_index.clear()
        tree.complete_matching_results.clear()
        tree.incomplete_matching_results.clear()

start()
