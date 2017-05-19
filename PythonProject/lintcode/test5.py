class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left, self.right = None, None
    def preorderTraversal(self, root):
            # write your code here
            p = [root]
            res = [0]
            while root is not None or len(p) != 1:
                res.append(root.val)
                if root.right is not None:
                    p.append(root.right)
                root = root.left
                if root == None and len(p) != 1:
                    root = p[len(p) - 1]
                    del p[len(p) - 1]
            n = len(res)
            return res[1:n]
if __name__ == '__main__':
    print self.sepreorderTraversal(TreeNode )