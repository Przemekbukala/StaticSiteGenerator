from textnode import *

""" It takes a list of "old nodes", a delimiter, and a text type, 
    where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax.
    :return: new list of nodes
    :type: list[TextNode]
"""
def split_nodes_delimiter(old_nodes : list[TextNode], delimiter: str, text_type : TextType):
    node: TextNode
    new_list=[]
    for i,node in enumerate(old_nodes):
        if node.text_type!=text_type.PLAIN_TEXT:
            new_list.append(node)
            continue
        splited_text=node.text.split(delimiter)
         #there is 3 cases, in which we could get from 1 to 3 nodes.
        if len(splited_text)==1 and len(splited_text)==2:
            raise Exception("Invalid Markdown syntax")
        if len(splited_text[0])==0 and len(splited_text[2])==0:
            new_list.append(TextNode(splited_text[1],text_type))
        elif  len(splited_text[0])==0:
            new_list.extend([TextNode(splited_text[1],text_type),TextNode(splited_text[2],node.text_type)])
        elif len(splited_text[2]) == 0:
            new_list.extend([TextNode(splited_text[0], node.text_type), TextNode(splited_text[1], text_type)])
        else:
            new_list.extend([TextNode(splited_text[0], node.text_type), TextNode(splited_text[1], text_type),TextNode(splited_text[2], node.text_type)])
    return new_list

if __name__=="__main__":
    node_test=TextNode("This is 'kod' a text node", TextType.PLAIN_TEXT)
    node_test_2=TextNode("This is 'kod a text node'", TextType.PLAIN_TEXT)
    nowa_lista=split_nodes_delimiter([node_test], "'", TextType.CODE_TEXT)
    nowa_listav2=split_nodes_delimiter([node_test_2], "'", TextType.CODE_TEXT)
    print(nowa_lista)
    print(nowa_listav2)
