# Node as dictionary
def make_node(key, left=None, right=None):
    return {"key": key, "left": left, "right": right}

# Right rotation
def rotate_right(x):
    y = x["left"]
    x["left"] = y["right"]
    y["right"] = x
    return y

# Left rotation
def rotate_left(x):
    y = x["right"]
    x["right"] = y["left"]
    y["left"] = x
    return y

# Splay operation
def splay(root, key):
    if root is None or root["key"] == key:
        return root

    # Key in left subtree
    if key < root["key"]:
        if root["left"] is None:
            return root
        if key < root["left"]["key"]:  # Zig-Zig
            root["left"]["left"] = splay(root["left"]["left"], key)
            root = rotate_right(root)
        elif key > root["left"]["key"]:  # Zig-Zag
            root["left"]["right"] = splay(root["left"]["right"], key)
            if root["left"]["right"]:
                root["left"] = rotate_left(root["left"])
        return root if root["left"] is None else rotate_right(root)

    else:  # Key in right subtree
        if root["right"] is None:
            return root
        if key < root["right"]["key"]:  # Zag-Zig
            root["right"]["left"] = splay(root["right"]["left"], key)
            if root["right"]["left"]:
                root["right"] = rotate_right(root["right"])
        elif key > root["right"]["key"]:  # Zag-Zag
            root["right"]["right"] = splay(root["right"]["right"], key)
            root = rotate_left(root)
        return root if root["right"] is None else rotate_left(root)

# Insert
def insert(root, key):
    if root is None:
        return make_node(key)
    root = splay(root, key)
    if root["key"] == key:
        return root
    new_node = make_node(key)
    if key < root["key"]:
        new_node["right"] = root
        new_node["left"] = root["left"]
        root["left"] = None
    else:
        new_node["left"] = root
        new_node["right"] = root["right"]
        root["right"] = None
    return new_node

# Search
def search(root, key):
    return splay(root, key)

# Delete
def delete(root, key):
    if root is None:
        return None
    root = splay(root, key)
    if root["key"] != key:
        return root
    if root["left"] is None:
        return root["right"]
    temp = root["right"]
    root = splay(root["left"], key)
    root["right"] = temp
    return root

# Inorder traversal
def inorder(root):
    if root:
        inorder(root["left"])
        print(root["key"], end=" ")
        inorder(root["right"])


# Example usage
if __name__ == "__main__":
    root = None
    for x in [10, 20, 30, 40, 50, 25]:
        root = insert(root, x)

    print("Inorder traversal after insertion:")
    inorder(root)
    print("\nSearching 25:")
    root = search(root, 25)
    print("Root after splaying:", root["key"])
    root = delete(root, 40)
    print("Inorder traversal after deleting 40:")
    inorder(root)
==================================================================================================================================================================




def create_node(t, leaf=False):
    return {"t": t, "leaf": leaf, "keys": [], "children": []}

def traverse(node):
    if node is None:
        return
    for i in range(len(node["keys"])):
        if not node["leaf"]:
            traverse(node["children"][i])
        print(node["keys"][i], end=" ")
    if not node["leaf"]:
        traverse(node["children"][len(node["keys"])])

def search(node, k):
    if node is None:
        return None
    i = 0
    while i < len(node["keys"]) and k > node["keys"][i]:
        i += 1
    if i < len(node["keys"]) and node["keys"][i] == k:
        return node
    if node["leaf"]:
        return None
    return search(node["children"][i], k)

def split_child(parent, i, t):
    y = parent["children"][i]
    z = create_node(t, y["leaf"])
    parent["children"].insert(i + 1, z)
    parent["keys"].insert(i, y["keys"][t - 1])
    z["keys"] = y["keys"][t:(2 * t - 1)]
    y["keys"] = y["keys"][0:(t - 1)]
    if not y["leaf"]:
        z["children"] = y["children"][t:(2 * t)]
        y["children"] = y["children"][0:t]

def insert_non_full(node, k, t):
    i = len(node["keys"]) - 1
    if node["leaf"]:
        node["keys"].append(0)
        while i >= 0 and k < node["keys"][i]:
            node["keys"][i + 1] = node["keys"][i]
            i -= 1
        node["keys"][i + 1] = k
    else:
        while i >= 0 and k < node["keys"][i]:
            i -= 1
        i += 1
        if len(node["children"][i]["keys"]) == (2 * t - 1):
            split_child(node, i, t)
            if k > node["keys"][i]:
                i += 1
        insert_non_full(node["children"][i], k, t)

def insert(root, k, t):
    if root is None:
        root = create_node(t, True)
        root["keys"].append(k)
        return root
    if len(root["keys"]) == (2 * t - 1):
        s = create_node(t, False)
        s["children"].append(root)
        split_child(s, 0, t)
        i = 0
        if s["keys"][0] < k:
            i += 1
        insert_non_full(s["children"][i], k, t)
        return s
    else:
        insert_non_full(root, k, t)
        return root


# Example usage
if __name__ == "__main__":
    t = 3
    root = None
    elements = [10, 20, 5, 6, 12, 30, 7, 17]
    for el in elements:
        root = insert(root, el, t)

    print("Traversal of B-Tree:")
    traverse(root)
    print("\nSearch 6:", "Found" if search(root, 6) else "Not Found")
    print("Search 15:", "Found" if search(root, 15) else "Not Found")






