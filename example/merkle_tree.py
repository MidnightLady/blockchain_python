from hashlib import sha256


class MerkleNode:
    """
    Stores the hash and the parent.
    """

    def __init__(self, hash256, chunk=None):
        self.chunk = chunk
        self.hash = hash256
        self.parent = None
        self.left_child = None
        self.right_child = None


class MerkleTree:
    leaves = None
    root = None

    """
    Stores the leaves and the root hash of the tree.
    """
    @staticmethod
    def compute_hash(data):
        data = data.encode('utf-8')
        return sha256(data).hexdigest()

    def __init__(self, data_chunks):
        self.leaves = []

        for chunk in data_chunks:
            node = MerkleNode(self.compute_hash(chunk), chunk=chunk)
            self.leaves.append(node)

        self.root = self.build_merkle_tree(self.leaves)

    def build_merkle_tree(self, nodes):
        """
        Builds the Merkle tree from a list of leaves. In case of an odd number of leaves, the last leaf is duplicated.
        """
        num_leaves = len(nodes)
        if num_leaves == 1:
            return nodes[0]

        parents = []

        i = 0
        while i < num_leaves:
            left_child = nodes[i]
            right_child = nodes[i + 1] if i + 1 < num_leaves else left_child

            parents.append(self.create_parent(left_child, right_child))

            i += 2

        return self.build_merkle_tree(parents)

    def create_parent(self, left_child, right_child):
        """
        Creates the parent node from the children, and updates
        their parent field.
        """
        parent = MerkleNode(self.compute_hash(left_child.hash + right_child.hash), left_child.chunk + right_child.chunk)
        left_child.parent, right_child.parent = parent, parent
        parent.left_child, parent.right_child = left_child, right_child

        return parent

    def get_audit_trail(self, chunk_hash):
        """
        Checks if the leaf exists, and returns the audit trail
        in case it does.
        """
        for leaf in self.leaves:
            if leaf.hash == chunk_hash:
                return self.generate_audit_trail(leaf, [])
        return False

    def generate_audit_trail(self, node, trail):
        """
        Generates the audit trail in a bottom-up fashion
        """
        if node == self.root:
            trail.append(node.hash)
            return trail

        # check if the merkle_node is the left child or the right child
        is_left = node.parent.left_child == node
        if is_left:
            # since the current node is left child, right child is
            # needed for the audit trail. We'll need this info later
            # for audit proof.
            trail.append((node.parent.right_child.hash, not is_left))
            return self.generate_audit_trail(node.parent, trail)
        else:
            trail.append((node.parent.left_child.hash, not is_left))
            return self.generate_audit_trail(node.parent, trail)


    def verify_audit_trail(self, chunk_hash, audit_trail=None):
        """
        Performs the audit-proof from the audit_trail received
        from the trusted server.
        """
        if not audit_trail:
            audit_trail = self.get_audit_trail(chunk_hash)

        proof_till_now = chunk_hash
        for node in audit_trail[:-1]:
            hash256 = node[0]
            is_left = node[1]
            if is_left:
                # the order of hash concatenation depends on whether the
                # the node is a left child or right child of its parent
                proof_till_now = self.compute_hash(hash256 + proof_till_now)
            else:
                proof_till_now = self.compute_hash(proof_till_now + hash256)

        # verifying the computed root hash against the actual root hash
        return proof_till_now == audit_trail[-1]



chunks = ['0', '1', '2', '3', '4', '5', '6']
merkle_tree = MerkleTree(chunks)
chunk_hash = MerkleTree.compute_hash("2")
check = merkle_tree.verify_audit_trail(chunk_hash)
print(check)
