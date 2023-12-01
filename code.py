class Node:
    def __init__(self, key, color, left=None, right=None, parent=None):
        self.key = key
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent


class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None, "B")
        self.root = self.NIL

    def left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right

        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent

        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        x.right = y
        y.parent = x

    def insert_fixup(self, z):
        while z.parent.color == "R":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == "R":
                    z.parent.color = "B"
                    y.color = "B"
                    z.parent.parent.color = "R"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)

                    z.parent.color = "B"
                    z.parent.parent.color = "R"
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == "R":
                    z.parent.color = "B"
                    y.color = "B"
                    z.parent.parent.color = "R"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)

                    z.parent.color = "B"
                    z.parent.parent.color = "R"
                    self.left_rotate(z.parent.parent)

        self.root.color = "B"

    def insert(self, key):
        z = Node(key, "R", self.NIL, self.NIL, self.NIL)
        y = self.NIL
        x = self.root

        while x != self.NIL:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y

        if y == self.NIL:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        self.insert_fixup(z)

    def delete_fixup(self, x):
        while x != self.root and x.color == "B":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "R":
                    w.color = "B"
                    x.parent.color = "R"
                    self.left_rotate(x.parent)
                    w = x.parent.right

                if w.left.color == "B" and w.right.color == "B":
                    w.color = "R"
                    x = x.parent
                else:
                    if w.right.color == "B":
                        w.left.color = "B"
                        w.color = "R"
                        self.right_rotate(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = "B"
                    w.right.color = "B"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "R":
                    w.color = "B"
                    x.parent.color = "R"
                    self.right_rotate(x.parent)
                    w = x.parent.left

                if w.right.color == "B" and w.left.color == "B":
                    w.color = "R"
                    x = x.parent
                else:
                    if w.left.color == "B":
                        w.right.color = "B"
                        w.color = "R"
                        self.left_rotate(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = "B"
                    w.left.color = "B"
                    self.right_rotate(x.parent)
                    x = self.root

        x.color = "B"

    def delete(self, key):
        z = self.search(key)
        if z == self.NIL:
            return

        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum_node(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "B":
            self.delete_fixup(x)

    def search(self, key):
        return self.search_recursive(self.root, key)

    def search_recursive(self, x, key):
        if x == self.NIL or key == x.key:
            return x

        if key < x.key:
            return self.search_recursive(x.left, key)
        else:
            return self.search_recursive(x.right, key)

    def minimum_node(self, x):
        while x.left != self.NIL:
            x = x.left
        return x

    def transplant(self, u, v):
        if u.parent == self.NIL:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent

    def maximum(self):
        return self.maximum_recursive(self.root)

    def maximum_recursive(self, x):
        while x.right != self.NIL:
            x = x.right
        return x

    def minimum(self):
        return self.minimum_recursive(self.root)

    def minimum_recursive(self, x):
        while x.left != self.NIL:
            x = x.left
        return x

    def displayTree(self, node, indent, last):
        if node != self.NIL:
            if node.parent != self.NIL:
                print(indent, end="")
                if last:
                    if node.parent.left == self.NIL:
                        print("└──", end="")
                    else:
                        print("├──", end="")
                    indent += "│  "
                else:
                    print("└──", end="")
                    indent += "   "

            print(f"{node.color}{node.key}")
            self.displayTree(node.right, indent, True)
            self.displayTree(node.left, indent, False)

    # to Print the tree
    def print_tree(self):
        self.displayTree(self.root, "", True)


def main():
    rb_tree = RedBlackTree()

    print("\nRed-Black Tree Operations:")
    print("\t1. Insert")
    print("\t2. Delete")
    print("\t3. Search")
    print("\t4. Maximum")
    print("\t5. Minimum")
    print("\t6. Print Tree")
    print("\t0. Exit")

    number_of_iterations = int(input("\nEnter the Number of Iterations: "))

    while number_of_iterations > 0:
        number_of_iterations -= 1
        print("\nCurrent Red-Black Tree:")
        rb_tree.print_tree()

        operations = input("\nEnter operations (e.g. '5 10 15 20 25 30 35 40 50' or 'Delete 35' or 'Max' or 'Min'): ")
        operation_list = operations.split()

        if operation_list[0].isdigit():
            values_to_insert = [int(value) for value in operation_list]
            for value in values_to_insert:
                rb_tree.insert(value)
        elif operation_list[0].lower() == "insert":
            value_to_insert = int(operation_list[1])
            rb_tree.insert(value_to_insert)
        elif operation_list[0].lower() == "delete":
            key_to_delete = int(operation_list[1])
            rb_tree.delete(key_to_delete)
        elif operation_list[0].lower() == "search":
            key_to_search = int(operation_list[1])
            result = rb_tree.search(key_to_search)
            print(result != rb_tree.NIL)
        elif operation_list[0].lower() == "max":
            max_node = rb_tree.maximum()
            print(max_node.key if max_node != rb_tree.NIL else 'Tree is empty')
        elif operation_list[0].lower() == "min":
            min_node = rb_tree.minimum()
            print(min_node.key if min_node != rb_tree.NIL else 'Tree is empty')
        elif operation_list[0].isdigit():
            num_operations = int(operation_list[0])
            for i in range(1, num_operations + 1):
                if operation_list[i * 2 - 1].lower() == "delete":
                    key_to_delete = int(operation_list[i * 2])
                    rb_tree.delete(key_to_delete)
                elif operation_list[i * 2 - 1].lower() == "insert":
                    value_to_insert = int(operation_list[i * 2])
                    rb_tree.insert(value_to_insert)
                else:
                    print("Invalid operation. Please enter a valid operation.")
        elif operation_list[0].lower() == "exit":
            print("Exiting the program.")
            break
        else:
            print("Invalid operation. Please enter a valid operation.")


if __name__ == "__main__":
    main()

