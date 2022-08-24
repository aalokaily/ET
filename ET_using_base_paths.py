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
				stack.append(last_node_under_top_node_in_stack)	  # append it to process later with the required order (postorder) and remove it from OSHR[current_node.key]
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

	building_start = time.time()
	
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
				nodes_stack.append(last_node_under_top_node_in_stack)	  # append it to process later with the required order (postorder) and remove it from OSHR[current_node.key]
				OSHR_leaf_nodes_counter_stack.append(OSHR_leaf_nodes_key_counter)
				OSHR_internal_nodes_counter_stack.append(OSHR_internal_nodes_key_counter)
				children_stack[-1].pop()					
				children_stack.append((list(last_node_under_top_node_in_stack.transition_links[x] for x in sorted(last_node_under_top_node_in_stack.transition_links.keys(), reverse=True))))
			else:
				# alongside processing
				if not current_node.is_leaf():
					#tree.temp[tree._edgeLabel(current_node, tree.root)]
					
					#find and mark inbetween top base node and assign the reference nodes for this node (which are as coded below)
					if current_node._suffix_link.parent != current_node.parent._suffix_link:
						top_node = current_node.parent._suffix_link 
						bottom_node = current_node._suffix_link
						
						n = bottom_node.parent
						while n  != top_node:
							if hasattr(n, "inbetween_top_base_node"):
								n.inbetween_top_base_node.append(current_node)
							else:
								setattr(n, "inbetween_top_base_node", [current_node])
							n = n.parent
							
					# index OSHR leaf and internal nodes under ST internal nodes	
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
		global text
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
				nodes_stack.append(last_node_under_top_node_in_stack)	  # append it to process later with the required order (postorder) and remove it from OSHR[current_node.key]
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


def find_approximate_matching(tree, pattern, required_k, starting_node, path_of_nodes_for_pattern, suffixes_traversals):
	# path_of_nodes_for_pattern contains the path of the pattern in ST
	# suffixes_traversals contains m elements where element at position i contain a tuple of (end_node, k, errors_positions) where end_node is the end node of the path of the ith suffix of the pattern in ST
	# k is the number of mismatches encountered on edges, and errors_positions is the position of mismatch found in the path. 
	pattern_length = len(pattern)
	
	complete_results = []
	incomplete_results = []  # this will stores the incomplete matching for current k but may be matching for k + 1 matching
	i = -1
	
	for node_info in path_of_nodes_for_pattern:
		i += 1
		main_node = node_info[0]
		depth_of_main_node = main_node.depth
		depth_from_starting_node = depth_of_main_node - starting_node.depth 
		depth_in_tree_to_look_for = pattern_length + starting_node.depth
		main_errors = node_info[1]
		main_errors_positions = node_info[2]
		latest_k_value_to_search_for = required_k - main_errors
		
		if latest_k_value_to_search_for == 0:	# then keep walking in the path until last node is reached and make the below check
			if  depth_of_main_node  >= depth_in_tree_to_look_for:
				if main_errors == required_k:
					complete_results.append((main_errors_positions, main_node))
					
		elif latest_k_value_to_search_for > 0:
			if depth_of_main_node  == depth_in_tree_to_look_for - latest_k_value_to_search_for: # then matching can be computed without OT index and just compute the branching below to the depth of latest_k_value_to_search_for (if depth_in_tree_to_look_for - latest_k_value_to_search_for < depth_of_main_node < depth_in_tree_to_look_for then no matching needed to be done)
				branching_letters_and_nodes = find_branching_letters_and_nodes_to_depth_k(main_node, latest_k_value_to_search_for)
				for transition_letters in branching_letters_and_nodes.keys():
					transition_node = branching_letters_and_nodes[transition_letters]
					mismatches = 0
					mismatches_positions = []
					for i, j in enumerate(Hamming_distance(transition_letters, pattern[depth_from_starting_node:depth_from_starting_node + latest_k_value_to_search_for])):
						if j == 1:
							mismatches += 1 
							mismatches_positions.append(i +  depth_from_starting_node)
					
					if mismatches == latest_k_value_to_search_for:
						complete_results.append((main_errors_positions + mismatches_positions, transition_node))
						
			elif  depth_of_main_node < depth_in_tree_to_look_for - latest_k_value_to_search_for:
				
				suffix_end_node = suffixes_traversals[depth_from_starting_node + latest_k_value_to_search_for][0]
				suffix_errors = suffixes_traversals[depth_from_starting_node + latest_k_value_to_search_for][1]
				suffix_errors_positions = suffixes_traversals[depth_from_starting_node + latest_k_value_to_search_for][2]
				
				latest_k_value_to_search_for = latest_k_value_to_search_for - suffix_errors
				if latest_k_value_to_search_for > 0 and suffix_end_node.depth > 0:#= depth_in_tree_to_look_for - (depth_of_main_node + latest_k_value_to_search_for): 
					branching_letters_and_nodes = find_branching_letters_and_nodes_to_depth_k(main_node, latest_k_value_to_search_for)
					
					for transition_letters in branching_letters_and_nodes.keys():
						transition_node = branching_letters_and_nodes[transition_letters]
						mismatches = 0
						mismatches_positions = []
						for i, j in enumerate(Hamming_distance(transition_letters, pattern[depth_from_starting_node:depth_from_starting_node + latest_k_value_to_search_for])):
							if j == 1:
								mismatches += 1 
								mismatches_positions.append(i + depth_from_starting_node)
						
						if mismatches == latest_k_value_to_search_for:
							if suffix_end_node.is_leaf(): # then the matching node, if any, must be a leaf node 
								key = tree.leaf_suffix_index_to_leaf_memory_list[suffix_end_node.idx - (depth_of_main_node + latest_k_value_to_search_for)].key # key_of_leaf_child_node with idx from root equal to transition_idx under current child_node
								if transition_node.is_leaf():
									if key == transition_node.key:
										complete_results.append((main_errors_positions + mismatches_positions + [x + depth_from_starting_node + latest_k_value_to_search_for + suffix_errors for x in suffix_errors_positions], transition_node))	
								
								else:								
									if key  >= transition_node.key_of_leftmost_leaf and key <= transition_node.key_of_rightmost_leaf:
										node = tree.leaf_suffix_index_to_leaf_memory_list[suffix_end_node.idx - transition_node.depth]
										if node.key >= transition_node.key_of_leftmost_leaf and node.key <= transition_node.key_of_rightmost_leaf:
											complete_results.append((main_errors_positions + mismatches_positions + [x + depth_from_starting_node + latest_k_value_to_search_for + suffix_errors for x in suffix_errors_positions], node))										
									
							else:
								if transition_node.is_leaf():
									if transition_node.depth >= depth_in_tree_to_look_for:
										if suffix_end_node.depth >= depth_in_tree_to_look_for - (depth_of_main_node + latest_k_value_to_search_for):
											key_of_leaf_node = tree.leaf_suffix_index_to_leaf_memory_list[transition_node.idx + depth_of_main_node + latest_k_value_to_search_for].key # key_of_leaf_node with idx starting from root equal to transition_idx under current node
											if key_of_leaf_node  >= suffix_end_node.key_of_leftmost_leaf and key_of_leaf_node <= suffix_end_node.key_of_rightmost_leaf:
												complete_results.append((main_errors_positions + mismatches_positions + [x + depth_from_starting_node + latest_k_value_to_search_for + suffix_errors for x in suffix_errors_positions], transition_node))
								
								else:
									approximate_matching_under_transition_node_was_not_found = True
									
									if transition_node.depth == depth_in_tree_to_look_for:
										if transition_node.depth == depth_of_main_node + latest_k_value_to_search_for:
											complete_results.append((main_errors_positions + mismatches_positions + [x + depth_from_starting_node + latest_k_value_to_search_for for x in suffix_errors_positions], transition_node))
											approximate_matching_under_transition_node_was_not_found = False
										
										elif transition_node.depth > depth_of_main_node + latest_k_value_to_search_for:
											idx_of_any_leaf_node_under_transition_node = tree.left_to_right_suffix_indexes_list[transition_node.key_of_leftmost_leaf]
											key_of_leaf_node = tree.leaf_suffix_index_to_leaf_memory_list[idx_of_any_leaf_node_under_transition_node + depth_of_main_node + latest_k_value_to_search_for].key 
											if key_of_leaf_node  >= suffix_end_node.key_of_leftmost_leaf and key_of_leaf_node <= suffix_end_node.key_of_rightmost_leaf:
												complete_results.append((main_errors_positions + mismatches_positions + [x + depth_from_starting_node + latest_k_value_to_search_for + suffix_errors for x in suffix_errors_positions], transition_node))
												approximate_matching_under_transition_node_was_not_found = False
										
									elif transition_node.depth > depth_in_tree_to_look_for:
										idx_of_any_leaf_node_under_transition_node = tree.left_to_right_suffix_indexes_list[transition_node.key_of_leftmost_leaf]
										key_of_leaf_node = tree.leaf_suffix_index_to_leaf_memory_list[idx_of_any_leaf_node_under_transition_node + depth_of_main_node + latest_k_value_to_search_for].key 
										if key_of_leaf_node  >= suffix_end_node.key_of_leftmost_leaf and key_of_leaf_node <= suffix_end_node.key_of_rightmost_leaf:
											complete_results.append((main_errors_positions + mismatches_positions + [x + depth_from_starting_node + latest_k_value_to_search_for + suffix_errors for x in suffix_errors_positions], transition_node))
											approximate_matching_under_transition_node_was_not_found = False
										
									else:                                              #transition_node.depth < depth_in_tree_to_look_for:
										# check if leaf node under transition_node is a matching node. This check is needed as leaf nodes is not covered by OT index of base paths. In the way, check the internal child nodes if they are matching nodes. If yes, then save the cost of OT index to finding these nodes are matching nodes as OT index of base paths cover internal nodes under transition_node 
										temp_suffix_end_node = None
										
										if transition_node.depth ==  depth_of_main_node + latest_k_value_to_search_for:
											temp_suffix_end_node = suffixes_traversals[transition_node.depth - starting_node.depth ][0]
											suffix_errors = suffixes_traversals[transition_node.depth - starting_node.depth ][1]
											suffix_errors_positions = suffixes_traversals[transition_node.depth - starting_node.depth ][2]
										else:
											idx_of_any_leaf_node_under_transition_node = tree.left_to_right_suffix_indexes_list[transition_node.key_of_leftmost_leaf]
											key_of_leaf_node = tree.leaf_suffix_index_to_leaf_memory_list[idx_of_any_leaf_node_under_transition_node + depth_of_main_node + latest_k_value_to_search_for].key # key_of_leaf_child_node with idx from root equal to transition_idx under current child_node
											if key_of_leaf_node  >= suffix_end_node.key_of_leftmost_leaf and key_of_leaf_node <= suffix_end_node.key_of_rightmost_leaf:
												temp_suffix_end_node = suffixes_traversals[transition_node.depth - starting_node.depth ][0]
												suffix_errors = suffixes_traversals[transition_node.depth - starting_node.depth ][1]
												suffix_errors_positions = suffixes_traversals[transition_node.depth - starting_node.depth ][2]
										
										if temp_suffix_end_node != None:
											temp = temp_suffix_end_node
											# firstly we need to check if the edge from depth_of_main_node + latest_k_value_to_search_for to depth of transition_node is matching with the correspondence string in the pattern
											# if matching, perform the matching using OT index under transition_node to find possible matching. If not, there is no need in the first place.
											matching_node = None
											for child_node in transition_node.transition_links.values():
												if child_node.depth >=  depth_in_tree_to_look_for and temp.depth >= pattern_length - (transition_node.depth - starting_node.depth): # the second condition to make sure the suffix walking was not stopped by no branching 
													if child_node.is_leaf():
														key_of_leaf_node = tree.leaf_suffix_index_to_leaf_memory_list[child_node.idx + transition_node.depth].key # key_of_leaf_child_node with idx from root equal to transition_idx under current child_node
														if key_of_leaf_node  >= temp_suffix_end_node.key_of_leftmost_leaf and key_of_leaf_node <= temp_suffix_end_node.key_of_rightmost_leaf:
															matching_node = child_node
													else:
														idx_of_any_leaf_node_under_transition_node = tree.left_to_right_suffix_indexes_list[child_node.key_of_leftmost_leaf]
														key_of_leaf_node = tree.leaf_suffix_index_to_leaf_memory_list[idx_of_any_leaf_node_under_transition_node + transition_node.depth].key # key_of_leaf_child_node with idx from root equal to transition_idx under current child_node
														if key_of_leaf_node  >= temp_suffix_end_node.key_of_leftmost_leaf and key_of_leaf_node <= temp_suffix_end_node.key_of_rightmost_leaf:
															matching_node = child_node
										
											deepest_matching_internal_node = None
											if matching_node == None:
												if transition_node.left_OT_index != transition_node.right_OT_index:  # if they are equal; then no OT indexing has been performed under this node and hence nothing to be done or matching to be computed
													f = True
													while temp_suffix_end_node != tree.root and f:
														left_position   =   bisect.bisect_left(temp_suffix_end_node.OT_indexes, transition_node.left_OT_index)
														right_position =   bisect.bisect_left(temp_suffix_end_node.OT_indexes, transition_node.right_OT_index)
														if left_position != right_position:
															f = False
															OT_index_of_a_base_path = temp_suffix_end_node.OT_indexes[left_position]
															guided_suffix = tree.OT_index[OT_index_of_a_base_path]
															suffix_to_search_for = guided_suffix - transition_node.depth
															key_of_suffix_to_search_for = tree.leaf_suffix_index_to_leaf_memory_list[suffix_to_search_for].key
															depth_required = temp_suffix_end_node.depth 
															
															deepest_matching_internal_node = find_end_node_given_suffix_key_and_depth(transition_node, key_of_suffix_to_search_for, depth_required)
															
															if deepest_matching_internal_node.depth >= depth_in_tree_to_look_for:
																matching_node = deepest_matching_internal_node
															else:
																for node in deepest_matching_internal_node.transition_links.values():
																	if node.is_leaf():
																		suffix_number_under_node = tree.leaf_suffix_index_to_leaf_memory_list[deepest_matching_internal_node.depth + node.idx]
																		end_node_of_suffix_starting_from_root = suffixes_traversals[deepest_matching_internal_node.depth - starting_node.depth][0]
																		if end_node_of_suffix_starting_from_root.is_leaf():
																			if suffix_number_under_node.key == end_node_of_suffix_starting_from_root.key:
																				matching_node = node
																		else:
																			if suffix_number_under_node.key  >= end_node_of_suffix_starting_from_root.key_of_leftmost_leaf and suffix_number_under_node.key <= end_node_of_suffix_starting_from_root.key_of_rightmost_leaf:
																				matching_node = node
																	else:
																		# get any index of leaf node under internal node
																		tt = tree.left_to_right_suffix_indexes_list[node.key_of_leftmost_leaf]
																		suffix_number_under_node = tree.leaf_suffix_index_to_leaf_memory_list[tt + deepest_matching_internal_node.depth]
																		end_node_of_suffix_starting_from_root = suffixes_traversals[deepest_matching_internal_node.depth - starting_node.depth][0]
																		if end_node_of_suffix_starting_from_root.is_leaf():
																			if suffix_number_under_node.key == end_node_of_suffix_starting_from_root.key:
																				matching_node = node
																		else:
																			if suffix_number_under_node.key  >= end_node_of_suffix_starting_from_root.key_of_leftmost_leaf and suffix_number_under_node.key <= end_node_of_suffix_starting_from_root.key_of_rightmost_leaf:
																				matching_node = node
																
																if matching_node == None:
																	matching_node = deepest_matching_internal_node
																	
														else:
															temp_suffix_end_node = temp_suffix_end_node.parent
											
											
											if matching_node != None:
												if temp.depth >= pattern_length - (transition_node.depth - starting_node.depth):
													if matching_node.depth >= depth_in_tree_to_look_for:
														complete_results.append((main_errors_positions + mismatches_positions + [x + depth_from_starting_node + latest_k_value_to_search_for + suffix_errors for x in suffix_errors_positions], matching_node))	
													else:
														incomplete_results.append((main_errors_positions + mismatches_positions + [x + depth_from_starting_node + latest_k_value_to_search_for + suffix_errors for x in suffix_errors_positions], matching_node))
												else:
													if deepest_matching_internal_node != None:
														incomplete_results.append((main_errors_positions + mismatches_positions + [x + depth_from_starting_node + latest_k_value_to_search_for + suffix_errors for x in suffix_errors_positions], deepest_matching_internal_node))
												
		
	return [complete_results, incomplete_results]
	
	
	
	
def print_results_given_list_of_node(tree, matching_nodes, pattern, pattern_length, k):
	#output _results
	
	print ("------------------------------------------------------------------------")
	print ("Approximate matchings:")
	print ("------------------------------------------------------------------------")
	
	if matching_nodes:
		tt = defaultdict(int)   # to hash apprximate matchings i order to check if the outcomes has duplicates. If the apprximate matching is correct, no duplicates should be preseneted in the approximate matchings. 
		position_combinations = defaultdict(int)
		i = 0
		different_dsitance = False
		matching_nodes.sort(key=lambda x: x[0])
		for it in matching_nodes:
			positions = it[0]
			matching_node = it[1]
			if matching_node.is_leaf():
				print (text[matching_node.idx :matching_node.idx + pattern_length], sum(Hamming_distance(text[matching_node.idx :matching_node.idx + pattern_length], pattern)),  positions, matching_node.idx, "leaf node")
				i += 1
				tt[matching_node.idx] += 1
				position_combinations["-".join([str(x) for x in positions])] = 0
				if k != sum(Hamming_distance(text[matching_node.idx :matching_node.idx + pattern_length], pattern)):
					different_dsitance = True
			else:
				for suffix_index in tree.left_to_right_suffix_indexes_list[matching_node.key_of_leftmost_leaf:matching_node.key_of_rightmost_leaf +1]: 
					print (text[suffix_index :suffix_index + pattern_length], sum(Hamming_distance(text[suffix_index :suffix_index + pattern_length], pattern)), positions, suffix_index)
					i += 1
					tt[suffix_index] += 1
					position_combinations["-".join([str(x) for x in positions])] = 0
					if k != sum(Hamming_distance(text[suffix_index :suffix_index + pattern_length], pattern)):
						different_dsitance = True

		if len(tt) != i:
			print ("ALERT: duplicates is preseneted in the approximate matchings", len(tt), i)
			for kk in tt:
				if tt[kk] > 1:
					print ("duplicate at position", kk)
		else:
			print ("\nNumber of matchings is", len(tt))
			#print ("No duplicates (results with same index in the reference text) is preseneted in the approximate matchings")
			print ("Number of position_combinations in the results", len(position_combinations))
			print ("Number of expected combinations", int(math.factorial(pattern_length)/(math.factorial(pattern_length-k) * math.factorial(k))))
			
		if i > 0: # means there was a result
			if different_dsitance:
				print ("There are matching results with distance different than", k)
			else:
				print ("All matching results is with a distance equal to", k, "as should be")
	else:
		print ("No apprximate matching found")
		
		
def find_end_node_of_each_suffix_of_pattern(tree, pattern, required_k):
	suffixes_traversals = []
	# compute suffixes paths of nodes
	pattern_length = len(pattern)
	
	path_of_nodes_for_pattern = find_all_nodes_in_path_of_string_starting_from_a_node(pattern, tree.root, required_k)
	suffixes_traversals.append(path_of_nodes_for_pattern[-1])
	#print (path_of_nodes_for_pattern[-1])
	#print (find_all_nodes_in_path_of_string_starting_from_a_node(pattern, tree.root, required_k)[-1])
	
	for i in range(1, pattern_length):
		previous_suffix_end_node_info = suffixes_traversals[-1]
		end_node_of_last_suffix = previous_suffix_end_node_info[0]
		k_value_of_last_suffix = previous_suffix_end_node_info[1]
		error_positions_of_last_suffix = previous_suffix_end_node_info[2]
		
		
		if end_node_of_last_suffix.is_leaf():
			node = end_node_of_last_suffix.parent._suffix_link
			k = 0
			errors_positions = []
			matching_start_pos = i + node.depth 

			for pos in error_positions_of_last_suffix:
				if pos <= node.depth and pos >= i:
					errors_positions.append(pos - 1)
					k += 1
					
			info =  find_all_nodes_in_path_of_string_starting_from_a_node(pattern[matching_start_pos:], node, required_k - k)
			end_node = info[-1][0]
			for pos in info[-1][2]:
				errors_positions.append(pos + node.depth)
				k += 1			

		else:
			if end_node_of_last_suffix._suffix_link.depth == pattern_length - i and (end_node_of_last_suffix.depth - 1) not in error_positions_of_last_suffix: # the second conditiont to avoid having the errors at last position as if so, the sufflk link will be not the right one
				end_node = end_node_of_last_suffix._suffix_link
				k = 0
				errors_positions = []
				for pos in error_positions_of_last_suffix:
					if pos < end_node.depth  and pos >= i:
						errors_positions.append(pos - 1)
						k += 1
						
			else:  # due to no transitions found in the current suffix path and may be found in next suffix path 
				node = end_node_of_last_suffix.parent._suffix_link
				k = 0
				errors_positions = []
				matching_start_pos = i + node.depth 
				for pos in error_positions_of_last_suffix:
					if pos <= node.depth  and pos >= i:
						errors_positions.append(pos - 1)
						k += 1

				info =  find_all_nodes_in_path_of_string_starting_from_a_node(pattern[matching_start_pos:], node, required_k - k)
				end_node = info[-1][0]
				for pos in info[-1][2]:
					errors_positions.append(pos + node.depth)
					k += 1				
				
		suffixes_traversals.append((end_node, k, errors_positions))
		
		#print (i, k,errors_positions,  tree._edgeLabel(end_node, tree.root)[:100])
		#print (find_all_nodes_in_path_of_string_starting_from_a_node(pattern[i:], tree.root, required_k)[-1])
	
	return suffixes_traversals
	

					
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


def find_all_nodes_in_path_of_string_starting_from_a_node(string, starting_node, required_k):		   
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
				edge_label = text[end_node.idx + current_node.depth:end_node.idx + current_node.depth + l]
			else:
				edge_label = text[end_node.idx + current_node.depth:end_node.idx + end_node.depth]
			
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


def find_branching_letters_and_nodes_to_depth_k(node, k):
	
	def recursive(node, depth, k):
		for child_node in node.transition_links.values():
			if child_node.depth - depth  < k :
				recursive(child_node, depth, k)
			else:
				results[text[child_node.idx + depth: child_node.idx + depth + k]] = child_node
	
	results = defaultdict()

	if k == 0:
		return ("Zero is no accepted value")
	elif k == 1:
		results = node.transition_links
	else:
		depth = node.depth
		recursive(node, depth, k) 

	return results
	

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
					end_node = child_node
					f = False
			else:
				if child_node.key_of_leftmost_leaf <= suffix_key <= child_node.key_of_rightmost_leaf:
					if child_node.depth - depth_of_starting_node == required_depth:
						node = None  # to stop the search
						end_node = child_node
						f = False
					else:
						node = child_node
							
	return end_node

#@profile  
		
global text
text = ""

def start():
	global text
	start_er = time.time()
	
	start = time.time()
	
	input_file = sys.argv[1]	
	K = int(sys.argv[2])
	pattern = sys.argv[3]
	
	if K > 0:
		with open(input_file) as file_in:		 
			for line in file_in:
				if line[0] != ">":
					text += line.strip() 

		print ("Reading input data took", round((time.time() - start), 5), "seconds")	
		print ("------------------------------------------------------------------------------------------")
		start = time.time()		
		tree = STree.STree(text)
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
		Build_OT_index(tree)
		

		start = time.time()
		
		starting_node = tree.root#.transition_links["A"].transition_links["A"].transition_links["A"].transition_links["C"]
		pattern = pattern
		pattern_length = len(pattern)
		depth_in_tree_to_look_for = pattern_length + starting_node.depth
		suffixes_traversals = find_end_node_of_each_suffix_of_pattern(tree, pattern, K)
		path_of_nodes_for_pattern_from_starting_node = find_all_nodes_in_path_of_string_starting_from_a_node(pattern, starting_node, 1)
		
		tree.complete_results = defaultdict()
		tree.incomplete_results = defaultdict()   # this dict to handle the incomplete matching that caused by no transition state (the pattern for instance has a character that is not within the alphabet of the input data)
		#first find adjacent complete_results
		for k_value in range (1, K + 1):
			tt = find_approximate_matching(tree, pattern, k_value, starting_node, path_of_nodes_for_pattern_from_starting_node, suffixes_traversals)
			tree.complete_results[k_value] = tt[0]
			tree.incomplete_results[k_value] = tt[1]
			#print_results_given_list_of_node(tree, tree.complete_results[k_value] , tree._edgeLabel(starting_node, tree.root) + pattern, pattern_length + starting_node.depth, K)
		
		
		for error_so_far in range (1, K):
			for res in tree.complete_results[error_so_far]:
				result_node = res[1]
				last_mismatch_position = res[0][-1] +  starting_node.depth
				#print (tree._edgeLabel(result_node, tree.root), "--------")
				#print (left_K_to_search_for)
				path_of_nodes = []
				new_starting_node = result_node.parent
				while new_starting_node.depth > last_mismatch_position + (1):
					path_of_nodes.append((new_starting_node, 0, []))
					new_starting_node = new_starting_node.parent
					
				path_of_nodes = path_of_nodes[::-1]
				#print (tree._edgeLabel(new_starting_node, tree.root), )	
				for left_K_to_search_for in range (1, K - error_so_far + 1):
					tt = find_approximate_matching(tree, pattern[new_starting_node.depth - starting_node.depth:], left_K_to_search_for, new_starting_node, path_of_nodes, suffixes_traversals[new_starting_node.depth - starting_node.depth:])
					for it in tt[0]:
						tree.complete_results[error_so_far + left_K_to_search_for].append((res[0] + [x + new_starting_node.depth for x in it[0]], it[1]))
						#print (tree._edgeLabel(it[1], tree.root)[:9])
					for it in tt[1]:
						tree.incomplete_results[error_so_far + left_K_to_search_for].append((res[0] + [x + new_starting_node.depth for x in it[0]], it[1]))
				
					#print_results_given_list_of_node(tree, tree.complete_results[error_so_far+left_K_to_search_for] , tree._edgeLabel(starting_node, tree.root) + pattern, pattern_length + starting_node.depth, K)
			
			if error_so_far < K:
				for res in tree.incomplete_results[error_so_far]:
					last_mismatch_position = res[0][-1] +  starting_node.depth
					result_node = res[1]
					path_of_nodes = [(result_node, 0, [])]
					#left_K_to_search_for = K - error_so_far
					
					#print (error_so_far, last_mismatch_position, left_K_to_search_for, tree._edgeLabel(result_node, tree.root)[:30])
					for left_K_to_search_for in range (1, K - error_so_far + 1):
						tt = find_approximate_matching(tree, pattern[result_node.depth - starting_node.depth:], left_K_to_search_for, result_node, path_of_nodes, suffixes_traversals[result_node.depth - starting_node.depth:])
						for it in tt[0]:
							tree.complete_results[error_so_far + left_K_to_search_for].append((res[0] + [x + result_node.depth for x in it[0]], it[1]))
						for it in tt[1]:
							tree.incomplete_results[error_so_far + left_K_to_search_for].append((res[0] + [x + result_node.depth for x in it[0]], it[1]))
				
				
		end_time = time.time()
		print_results_given_list_of_node(tree, tree.complete_results[K] , tree._edgeLabel(starting_node, tree.root) + pattern, depth_in_tree_to_look_for, K)	
		
		
		for k_value in range (1, K + 1):
			pass
			#print (k_value)
			#print_results_given_list_of_node(tree, tree.complete_results[k_value] , tree._edgeLabel(starting_node, tree.root) + pattern, pattern_length + starting_node.depth, k_value)
			#print_results_given_list_of_node(tree, tree.incomplete_results[k_value] , tree._edgeLabel(starting_node, tree.root) + pattern, pattern_length + starting_node.depth, k_value)
		
		print ("Found approximate matching for k =", K, "in ", round((end_time - start), 5), "seconds")
		
		
						
		delattr(tree, "leaf_suffix_index_to_leaf_memory_list")
		delattr(tree, "left_to_right_suffix_indexes_list")
		delattr(tree, "OSHR_leaf_nodes_left_to_right_list")
		delattr(tree, "OSHR_internal_nodes_left_to_right_list")
	else:
		print ("Please choose K value to be greater than 0")
	
	
		
start()
