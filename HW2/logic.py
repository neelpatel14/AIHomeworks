# Anirudh Ryali (ar9fh)

import Queue

class Step(object):
    def __init__(self, statement):
        self.statement = statement
        self.parent = None
        self.child = None
        self.left = None
        self.right = None
        self.width = len(self.statement)

queue = []

def construct_tree(string):
    del queue[:]
    split = string.split(", ")
    root = Step(split[0].strip())
    insatis = False
    if len(split) > 1:
        for i in range(1, len(split) - 1):
            queue.append(split[i])
        temp_node = Step(split[0].strip())
        insatis = build_tree(temp_node, 0, set())
        if insatis:
            print("")
            print_tree(temp_node)
            print("")
            print("Premises are insatisfiable, so invalid")
        queue.append("NEG ( " + split[-1] + " )")
    if insatis:
        return
    valid = build_tree(root, 0, set())
    print("")
    print_tree(root)
    if len(split) > 1:
        if valid:
            string += " is valid"
        else:
            string += " is not valid"
        print(string)

def print_tree(root):
    q = Queue.Queue()
    q.put(root)
    node = None
    while True:
        level_len = q.qsize()
        level_str = ""
        separ_str = ""
        non_int_found = False
        for i in range(level_len):
            node = q.get()
            if isinstance(node, int):
                level_str += ' ' * node
                separ_str += ' ' * node
                q.put(node)
            else:
                #print("DEBUG " + node.statement)
                non_int_found = True
                left_spaces = (node.width - len(node.statement))/2
                rite_spaces = node.width - len(node.statement) - left_spaces
                level_str += ' ' * left_spaces
                level_str += node.statement
                level_str += ' ' * rite_spaces
                #print("DEBUG  2" + level_str)
                if node.left == None and node.child == None:
                    q.put(node.width)
                    separ_str += ' ' * node.width
                elif node.left == None:
                    if node.child.width < node.width:
                        node.child.width = node.width
                    q.put(node.child)
                    left_separ = ( node.width - 1 ) / 2
                    separ_str += ' ' * left_separ
                    separ_str += '|'
                    separ_str += ' ' * ( node.width - 1 - left_separ )
                else:
                    left_pad = 0
                    rite_pad = 0
                    if node.left.width + 4 + node.right.width < node.width:
                        left_pad = (node.width - (node.left.width + 4 + node.right.width))/2
                        rite_pad = node.width - (node.left.width + 4 + node.right.width) - left_pad
                    if left_pad != 0:
                        q.put(left_pad)
                    q.put(node.left)
                    q.put(4)
                    q.put(node.right)
                    if rite_pad != 0:
                        q.put(rite_pad)
                    separ_str += ' ' * ( left_pad )
                    separ_str += ' ' * ( ( ( node.left.width - 1 ) / 2 ) + 1 )
                    separ_str += '/'
                    separ_str += ' ' * ( node.left.width - 1 - ( node.left.width - 1 ) / 2 + 2 + ( node.right.width - 1 ) / 2 )
                    separ_str += '\\' 
                    separ_str += ' ' * ( node.right.width - ( node.right.width - 1 ) / 2 )
                    separ_str += ' ' * ( rite_pad )

                    level_str = level_str[:(-1*(left_spaces + len(node.statement) + rite_spaces))]
                    left_dash = max( 0, left_spaces - ( left_pad + ( node.left.width - 1 ) / 2 + 1 ) - 1 )
                    rite_dash = max( 0, rite_spaces - ( rite_pad +node.right.width - ( node.right.width - 1 ) / 2 ) - 1 )
                    level_str += ' ' * ( left_spaces - left_dash ) +  '-' * left_dash
                    level_str += node.statement
                    level_str += '-' * rite_dash + ' ' * ( rite_spaces - rite_dash )
        if not non_int_found:
            break
        else:
            print(level_str)
            print(separ_str)


def build_tree(node, ind, statement_set):
    # Add equals

    no_par_without_neg = ""
    neg_front_offset = 0
    neg_back_offset = 0

    node.statement = remove_outer_parantheses(node.statement)
    if len(node.statement) > 4 and node.statement[:3] == "NEG":
        without_neg = node.statement[4:]
        no_par_without_neg = remove_outer_parantheses(without_neg)
        if without_neg != no_par_without_neg:
            node.statement = "NEG ( " + no_par_without_neg + " )"
            neg_front_offset = 6
            neg_back_offset -= 2
        else:
            node.statement = remove_outer_parantheses(node.statement)

    remove_node = node.statement not in statement_set
    statement_set.add(node.statement)

    node.width = len(node.statement)
    neg_back_offset += len(node.statement)

    split = node.statement.split(" ")
    if neg_front_offset == 6:
        split.pop(0)
        split.pop(0)
        split.pop()
    reverse_order = ["ARROW", "OR", "AND"]
    break_loop = False
    closed = True
    validity_str = ""
    for i in range(len(reverse_order)):
        par = 0
        length = 0
        for split_str in split:
            if split_str == "(":
                par += 1
            elif split_str == ")":
                par -= 1
            elif par == 0 and split_str == reverse_order[i]:
                break_loop = True
                left_str = node.statement[neg_front_offset : length + neg_front_offset - 1]
                rite_str = node.statement[(length + neg_front_offset + len(reverse_order[i]) + 1) : neg_back_offset]
                if i == 0:
                    if neg_front_offset == 0:           # Implication
                        node.left = Step( "NEG ( " + remove_outer_parantheses( left_str ) + " )" )
                        node.left.parent = node
                        node.right= Step( rite_str )
                        node.right.parent = node
                        node.width = max(node.width, node.left.width + node.right.width + 4)
                    else:                               # Negated Implication
                        rite_str = "NEG ( " + remove_outer_parantheses( rite_str ) + " )"
                elif i == 1:
                    if neg_front_offset == 0:           # Disjunction
                        node.left = Step( left_str )
                        node.left.parent = node
                        node.right= Step( rite_str )
                        node.right.parent = node
                    else:                               # Negated Disjunction
                        left_str = "NEG ( " + remove_outer_parantheses( left_str ) + " )"
                        rite_str = "NEG ( " + remove_outer_parantheses( rite_str ) + " )"
                else:
                    if neg_front_offset != 0:                               # Negated Conjunction
                        node.left = Step( "NEG ( " + remove_outer_parantheses( left_str ) + " )" )
                        node.left.parent = node
                        node.right= Step( "NEG ( " + remove_outer_parantheses( rite_str ) + " )" )
                        node.right.parent = node
                if node.left == None:
                    if left_str not in statement_set:
                        queue.append( left_str )
                    if rite_str not in statement_set and rite_str != left_str:
                        queue.append( rite_str )
                    if len(queue) > ind:
                        node.child = Step(queue[ind])
                        node.child.parent = node
                        closed = build_tree(node.child, ind + 1, statement_set)
                        node.width = max(node.width, node.child.width)
                    if rite_str not in statement_set and rite_str != left_str:
                        queue.pop()
                    if left_str not in statement_set:
                        queue.pop()
                else:
                    closed = build_tree(node.left, ind, statement_set)
                    closed = build_tree(node.right, ind, statement_set) and closed
                    node.width = max(node.width, node.left.width + node.right.width + 4)
                break
            length += len(split_str) + 1
        if break_loop:
            break

    if not break_loop:
        if neg_front_offset == 6:
            if remove_node:
                statement_set.remove(node.statement)
            node.statement = "NEG " + no_par_without_neg 
            remove_node = node.statement not in statement_set
            statement_set.add(node.statement)
            
        split = node.statement.split(" ")
        if split[0] == "NEG" and split[1] == "NEG" and ( node.statement[8:] not in statement_set ):
            node.child = Step(node.statement[8:])
            node.child.parent = node
            closed = build_tree(node.child, ind, statement_set)
            node.width = max(node.width, node.child.width)
        else:
            # Atomic so check if there is a contradiction
            contra = "NEG " + node.statement
            if len(contra) >= 8 and contra[:8] == "NEG NEG ":
                contra = remove_outer_parantheses(contra[8:])
            temp = node.parent
            contra_found = False
            while temp != None and not contra_found:
                if temp.statement == contra:
                    contra_found = True
                temp = temp.parent
            if contra_found:
                validity_str = "X"
                node.width = len(node.statement)
                closed = True
            elif len(queue) > ind:
                while ind < len(queue) and remove_outer_parantheses(queue[ind]) in statement_set:
                    ind += 1
                if ind < len(queue):
                    node.child = Step(queue[ind])
                    node.child.parent = node
                    closed = build_tree(node.child, ind + 1, statement_set)
                    node.width = max(node.width, node.child.width)
            if not contra_found and ind >= len(queue):
                validity_str = "O"
                node.width = len(node.statement)
                closed = False

    if remove_node:
        statement_set.remove(node.statement)

    if validity_str != "":
        node.statement += validity_str
        node.width = len(node.statement)

    return closed

        

if __name__ == "__main__":
    print("")
    print("Enter your argument, seperate statements with ', ' and separate every")
    print("variable, and operator by one space. Quantifiers, functions, and")
    print("predicates are NOT functional yet. Will be implemented by homework 3.")
    print("Enter 'QUIT' to exit the program")
    print("Valid inputs: ")
    print("'a OR b, a, b' -> invalid argument")
    print("'a AND ( b ARROW c ), a, NEG c, NEG b' -> valid argument")
    print("Invalid inputs: ")
    print("'(a AND b)' should be '( a AND b )'")
    print("'FORALL a Pa' since predicates and quantifiers are not implemented yet.")
    print("")
    while True:
        logic_string = raw_input("Enter a well-formed statement: ")
        if(logic_string == "QUIT"):
            print("Program exiting\n")
            break
        construct_tree(logic_string)
        print("\n")
