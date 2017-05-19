# coding:utf8
class TreeNode:
    def __init__(self, value=None, leftNode=None, rightNode=None):
        self.value = value
        self.leftNode = leftNode
        self.rightNode = rightNode
class Tree:
    def __init__(self,root=None):
        self.root = root
    def preOrder(self):
        if not self.root:
            return
        stackNode = []
        stackNode.append(self.root)
        while stackNode:
            node = stackNode.pop()
            print node.value,
            if node.rightNode:
                stackNode.append(node.rightNode)
            if node.leftNode:
                stackNode.append(node.leftNode)
    def midOrder(self):
        if not self.root:
            return
        stackNode = []
        node = None
        node = self.root
        while stackNode or node:
            while node:
                stackNode.append(node)
                node = node.leftNode
            node = stackNode.pop()
            print node.value,
            node = node.rightNode
    def aftOrder(self):
        if not self.root:
            return
        stackNode = []
        markNode = None
        node = self.root
        while stackNode or node:
            while node:
                stackNode.append(node)
                node = node.leftNode
            node = stackNode.pop()
            if not node.rightNode or node.rightNode is markNode:
                print node.value,
                markNode = node
                node = None
            else:
                stackNode.append(node)
                node = node.rightNode
if __name__ is '__main__':
    n10 = TreeNode(10,0,0)
    n9 = TreeNode(9,0,0)
    n3 = TreeNode(3,n9,n10)
    n8 = TreeNode(8,0,0)
    n14 = TreeNode(14,0,0)
    n7 = TreeNode(7,0,0)
    n16 = TreeNode(16,n7,0)
    n2 = TreeNode(2,n14,n8)
    n1 = TreeNode(1,n2,n16)
    root = TreeNode(4,n1,n3)
    tree = Tree(root)

    tree.preOrder()