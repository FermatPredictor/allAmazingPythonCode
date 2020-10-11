# -*- coding: utf-8 -*-
"""
程式功能:
給定一個二元樹，分別用不同的遍歷方式遍歷。
(過HackerRank的測試)
(LeetCode 94, 102, 144, 145題)

實作四種遍歷BST的方式:
前序遍歷 (Preorder Traversal，又稱DFS) 
中序遍歷 (Inorder Traversal) 
後序遍歷 (Postorder Traversal) 
層序遍歷 (Level-order Traversal，又稱BFS)
"""

class Node:
    def __init__(self,data):
        self.right=self.left=None
        self.data = data        

# root的高度為0
def getHeight(root):
    return -1 if not root else max(1+getHeight(root.left), 1+getHeight(root.right))

#回傳列表表示遍歷過的node的值
def preOrder(root):
    return [root.data]+preOrder(root.left)+preOrder(root.right) if root else []

def inOrder(root):
    return inOrder(root.left)+[root.data]+inOrder(root.right) if root else []
        
def postOrder(root):
    return postOrder(root.left)+postOrder(root.right)+[root.data] if root else []

def levelOrder(root):
    allLevel = []
    lvl = [root] if root else []
    while lvl:
        allLevel.append(list(map(lambda n: n.val, lvl)))
        lvl = [c for node in lvl for c in (node.left, node.right) if c]
    return allLevel
        
            
# 視覺化把樹印出height層
def printTree(root, height, appender=""):
    if not root or height<0:
        return
    print(appender,root.data);
    printTree(root.left, height-1, "   " + appender)
    printTree(root.right, height-1,"   " + appender)

