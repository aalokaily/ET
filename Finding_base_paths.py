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
            
                #find and mark inbetween top base node and assign the reference nodes for this node (which are as coded below)
                if current_visited_node._suffix_link.parent != current_visited_node.parent._suffix_link:
                    top_node = current_visited_node.parent._suffix_link 
                    bottom_node = current_visited_node._suffix_link

                    n = bottom_node.parent
                    while n  != top_node:
                        if not hasattr(n, "List_of_reference_internal_nodes"):
                            setattr(n, "List_of_reference_internal_nodes", [])
                        n.List_of_reference_internal_nodes.append(current_visited_node)
                        n = n.parent

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
    

   
def get_internal_nodes(tree, node):
    
    nodes_stack = []
    children_stack = []
    
    def preprocessing(tree):
        
        #iterative processing
        nodes_stack.append(node)
        children_stack.append((list(node.transition_links[x] for x in sorted(node.transition_links.keys(), reverse=True))))
        
        while nodes_stack:
            current_visited_node = nodes_stack[-1]                  
            if len(children_stack[-1]) > 0:
                last_node_under_top_node_in_stack = children_stack[-1][-1]
                #iterative processing
                nodes_stack.append(last_node_under_top_node_in_stack)   # append it to process later with the required order (postorder) and remove it from OSHR[current_visited_node.index_of_leaf_in_ST]
                children_stack[-1].pop()                    
                children_stack.append((list(last_node_under_top_node_in_stack.transition_links[x] for x in sorted(last_node_under_top_node_in_stack.transition_links.keys(), reverse=True))))
                                          
            else:
                # alongside processing
                if not current_visited_node.is_leaf():
                    results.append(current_visited_node)
                
                    
                #iterative processing 
                nodes_stack.pop()
                children_stack.pop()
                
    
    results = []
    preprocessing(tree)
    return results[:-1]


print ("Finding base paths using the proposed algorithm")

def Find_base_suffixes_using_linear_algorithm(tree):

    print ("Indexing OSHR leaf nodes into a list from left to right")
    
    setattr(tree, "List_of_OSHR_leaf_nodes_from_left_to_right", []) 
     
    cost = 0
    OSHR_leaf_nodes_key_counter = 0
    OSHR_internal_nodes_key_counter = 0

    nodes_stack = []
    OSHR_leaf_nodes_counter_stack = []
    children_stack = []

    #iterative processing
    nodes_stack.append(tree.root)
    OSHR_leaf_nodes_counter_stack.append(0)
    children_stack.append((list(tree.root.transition_links[x] for x in sorted(tree.root.transition_links.keys(), reverse=True))))
    
    while nodes_stack:
        cost += 1
        current_visited_node = nodes_stack[-1]                
        if len(children_stack[-1]) > 0:
            last_node_under_top_node_in_stack = children_stack[-1][-1]
            #iterative processing
            nodes_stack.append(last_node_under_top_node_in_stack)     # append it to process later with the required order (postorder) and remove it from OSHR[current_visited_node.key]
            OSHR_leaf_nodes_counter_stack.append(OSHR_leaf_nodes_key_counter)
            children_stack[-1].pop()                    
            children_stack.append((list(last_node_under_top_node_in_stack.transition_links[x] for x in sorted(last_node_under_top_node_in_stack.transition_links.keys(), reverse=True))))
        else:
            # alongside processing
            if not current_visited_node.is_leaf():
                # index OSHR leaf and OSHR internal nodes under ST internal nodes    
                setattr(current_visited_node, "index_of_leftmost_OSHR_leaf", OSHR_leaf_nodes_counter_stack[-1])
                setattr(current_visited_node, "index_of_rightmost_OSHR_leaf", OSHR_leaf_nodes_key_counter - 1)
            
                if hasattr(current_visited_node, "List_of_nodes_suffix_linked_to_me"):
                    OSHR_internal_nodes_key_counter += 1
                    
                    # The follwing new list will be needed in next phase
                    setattr(current_visited_node, "List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST", [])
                    for node in current_visited_node.List_of_nodes_suffix_linked_to_me:
                        current_visited_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST.append((node.index_of_leftmost_leaf_in_ST, node.index_of_rightmost_leaf_in_ST, node))
                        cost += 1
                    current_visited_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST.sort(key=lambda element: (element[0], element[1]))
                
                else:
                    tree.List_of_OSHR_leaf_nodes_from_left_to_right.append(current_visited_node)
                    OSHR_leaf_nodes_key_counter += 1
            
            
            #iterative processing
            OSHR_leaf_nodes_counter_stack.pop()
            nodes_stack.pop()
            children_stack.pop()

    print ("Number of OSHR leaf_nodes is", "{:,}".format(OSHR_leaf_nodes_key_counter))
    print ("Number of OSHR internal nodes is", "{:,}".format(OSHR_internal_nodes_key_counter))
    print ( "In total of", "{:,}".format(OSHR_leaf_nodes_key_counter + OSHR_internal_nodes_key_counter))
    print ("Cost for indexing OSHR leaf nodes into a list from left to right and sorting all List_of_nodes_suffix_linked_to_me:", "{:,}".format(cost))
    
    # ------------------------------------------------------------------------ find base paths -------------------------------------------------------------------------
    print ("Finding base paths")
    nodes_stack = []
    children_stack = []
    
    nodes_stack.append(tree.root)
    children_stack.append((list(tree.root.List_of_nodes_suffix_linked_to_me)))
    
    base_paths_counter = 0
    a1, a2, b1, b2 = 0, 0, 0, 0
    
    while nodes_stack:
        cost += 1
        current_visited_node = nodes_stack[-1]
        #check if OSHR[current_visited_node.key] is empty, then remove it from nodes_stack
        if len(children_stack[-1]) > 0:
            last_node_under_top_node_in_stack = children_stack[-1][-1]
            nodes_stack.append(last_node_under_top_node_in_stack)     
            children_stack[-1].pop()
            if hasattr(last_node_under_top_node_in_stack, "List_of_nodes_suffix_linked_to_me"):
                children_stack.append((list(last_node_under_top_node_in_stack.List_of_nodes_suffix_linked_to_me)))
            else:
                children_stack.append([])
            
        else:
            # the following 6 lines cover a special case and for the root only. The suffix-link of child internal node of a root usually link to the root. In case not, 
            # then the node that the child internal node link to must be bottom-node for the root node.
            setattr(current_visited_node, "List_of_bottom_base_node", [])
            if current_visited_node != tree.root:
                if hasattr(current_visited_node, "List_of_nodes_suffix_linked_to_me"):
                    # collect and find base paths based on OSHR leaf nodes
                    for bottom_base_node in tree.List_of_OSHR_leaf_nodes_from_left_to_right[current_visited_node.index_of_leftmost_OSHR_leaf:current_visited_node.index_of_rightmost_OSHR_leaf + 1]:
                        current_visited_node.List_of_bottom_base_node.append(bottom_base_node)
                        base_paths_counter += 1
                        a1 += 1
                        cost += 1
                    
                    # collect bottom-base nodes collected from reference nodes if current_visited_node is List_of_reference_internal_nodes 
                    inbetween_bottom_base_node_dict = defaultdict()  # this dict will be used to distinct nodes under tow difference reference nodes that are linking to the same node under current_visited_node                   
                    if hasattr(current_visited_node, "List_of_reference_internal_nodes"):
                        for reference_node in current_visited_node.List_of_reference_internal_nodes:
                            inbetween_bottom_base_node_dict[reference_node._suffix_link] = reference_node._suffix_link
                            cost += 1
                            for node in get_internal_nodes(tree, reference_node):
                                inbetween_bottom_base_node_dict[node._suffix_link] = node._suffix_link
                                cost += 1
                            
                    for bottom_base_node in list(inbetween_bottom_base_node_dict.values()):
                        cost += 1
                        f = 0
                        for node_with_suffix_link_to_current_visited_node in current_visited_node.List_of_nodes_suffix_linked_to_me:
                            cost += int(math.log(len(bottom_base_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST), 2))
                            right_pos = bisect.bisect(bottom_base_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST, (node_with_suffix_link_to_current_visited_node.index_of_rightmost_leaf_in_ST, node_with_suffix_link_to_current_visited_node.index_of_rightmost_leaf_in_ST)) # right_pos bcus we want to find node satisfies the condition starting_node.left_OT_index >= node.left_OT_index and starting_node.right_OT_index <= node.right_OT_index
                            if right_pos != 0:
                                right_pos = right_pos - 1
                            node_with_suffix_link_to_bottom_base_node = bottom_base_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST[right_pos][2]
                            if node_with_suffix_link_to_current_visited_node.index_of_leftmost_leaf_in_ST <= node_with_suffix_link_to_bottom_base_node.index_of_leftmost_leaf_in_ST <= node_with_suffix_link_to_bottom_base_node.index_of_rightmost_leaf_in_ST <= node_with_suffix_link_to_current_visited_node.index_of_rightmost_leaf_in_ST:
                                f = 1 # then it's already covered by previous base path
                                break
                                    
                        if f == 0:
                            a2 += 1
                            current_visited_node.List_of_bottom_base_node.append(bottom_base_node)
                            base_paths_counter += 1
                        
                else:
                    for bottom_base_node in get_internal_nodes(tree, current_visited_node):
                        current_visited_node.List_of_bottom_base_node.append(bottom_base_node)
                        base_paths_counter += 1
                        cost += 1
                            
                        if hasattr(bottom_base_node, "List_of_nodes_suffix_linked_to_me"):
                            b2 += 1
                        else:
                            b1 += 1
                            
                    
            nodes_stack.pop()
            children_stack.pop()

    print ("Number of OSHR leaf bottom base nodes for OSHR internal top base nodes", "{:,}".format(a1))
    print ("Number of OSHR internal bottom base nodes for OSHR internal top base nodes", "{:,}".format(a2))
    print ("Number of OSHR leaf bottom base nodes for OSHR leaf top base nodes", "{:,}".format(b1))
    print ("Number of OSHR internal bottom base nodes for OSHR leaf top base nodes", "{:,}".format(b2))
    print ()
    print ("Total number of base paths", "{:,}".format(base_paths_counter))
    print ("Total time cost:", "{:,}".format(cost))
    
    
start = time.time()
Find_base_suffixes_using_linear_algorithm(tree)
print ("Finished in", round((time.time() - start), 5), "seconds")
print ("------------------------------------------------------------------------------------------")
    


def Find_and_check_base_suffixes_using_non_trivial_algorithm(tree):
    
    print ("Finding and checking base paths using the non-trivial algorithm")

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
            if current_visited_node != tree.root:
                if not current_visited_node.is_leaf(): 
                    d = []
                    if hasattr(current_visited_node, "List_of_nodes_suffix_linked_to_me"):
                        for internal_node in get_internal_nodes(tree, current_visited_node):
                            cost += 1
                            if hasattr(internal_node, "List_of_nodes_suffix_linked_to_me"):
                                f = 0
                                for node_with_suffix_link_to_internal_node in internal_node.List_of_nodes_suffix_linked_to_me:
                                    cost += int(math.log(len(current_visited_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST),2)) 
                                    right_pos = bisect.bisect(current_visited_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST, (node_with_suffix_link_to_internal_node.index_of_rightmost_leaf_in_ST, node_with_suffix_link_to_internal_node.index_of_rightmost_leaf_in_ST)) # right_pos bcus we want to find node satisfies the condition starting_node.left_OT_index >= node.left_OT_index and starting_node.right_OT_index <= node.right_OT_index
                                    if right_pos != 0:
                                        right_pos = right_pos - 1
                                    node_with_suffix_link_to_current_visited_node = current_visited_node.List_of_nodes_suffix_linked_to_me_sorted_by_leaf_index_under_ST[right_pos][2]
                                    if node_with_suffix_link_to_current_visited_node.index_of_leftmost_leaf_in_ST <= node_with_suffix_link_to_internal_node.index_of_leftmost_leaf_in_ST <= node_with_suffix_link_to_internal_node.index_of_rightmost_leaf_in_ST <= node_with_suffix_link_to_current_visited_node.index_of_rightmost_leaf_in_ST:
                                        f = 1 
                                        break
                                                
                                if f == 0:
                                    d.append(internal_node)
                            else:
                                d.append(internal_node)
                                
                    else:
                        for internal_node in get_internal_nodes(tree, current_visited_node):
                            d.append(internal_node)
                            cost += 1
                
                        
                #if sorted([str(x) for x in d]) != sorted([str(x) for x in current_visited_node.List_of_bottom_base_node]):
                #    print ("The two base paths lists of this internal node are different", current_visited_node, tree._edgeLabel(current_visited_node, tree.root), "\n", sorted([tree._edgeLabel(x, current_visited_node) for x in d]), "\n", sorted([tree._edgeLabel(x, current_visited_node) for x in current_visited_node.List_of_bottom_base_node]))  
                #    flag = 1
                    
            nodes_stack.pop()
            children_stack.pop()

    if flag == 0:
        print ("=== All base paths at each internal nodes in ST are as expected ===")
        print ("Total time cost:", "{:,}".format(cost))
    else:
        print ("*** There are base paths lists that are different at some internal nodes***")
    
    
start = time.time()    
Find_and_check_base_suffixes_using_non_trivial_algorithm(tree)
print ("Finished in", round((time.time() - start), 5), "seconds")
   

 