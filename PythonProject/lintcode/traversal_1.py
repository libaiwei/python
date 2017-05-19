# coding:utf8
class Tree(object):
    def __init__(self,data,left,right):
        self.data=data
        self.left=left
        self.right=right
def post_visit(Tree):
    if Tree:
        post_visit(Tree.left)
        post_visit(Tree.right)
        print Tree.data
def pre_visit(Tree):
    if Tree:
        print Tree.data
        pre_visit(Tree.left)
        pre_visit(Tree.right)
def in_visit(Tree):
    if Tree:
        in_visit(Tree.left)
        print Tree.data
        in_visit(Tree.right)
node1=Tree(1,0,0)
node2=Tree(2,0,0)
node3=Tree(3,node1,node2)
node4=Tree(4,0,0)
node5=Tree(5,node4,node3)
print "the post_visit is ....."
post_visit(node5)

print "the pre_visit is......."
pre_visit(node5)
print "the in_visit is ......."
in_visit(node5)