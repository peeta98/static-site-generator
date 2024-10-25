class HTMLNode:
  def __init__(self, tag=None, value=None, children=None, props=None):
    self.tag = tag # e.g. <p>
    self.value = value # e.g. "Text between the <p> tags"
    self.children = children # e.g. Any HTML node objects representing the children of this node
    self.props = props # e.g. Attributes of the HTML tag {"href": "https://google.com"}

  def __repr__(self):
      return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

  def to_html(self):
    raise NotImplementedError

  def props_to_html(self):
    if self.props is None:
      return ""
    html_attributes = [f'{key}="{value}"' for key, value in self.props.items()]
    return " " + " ".join(html_attributes)
  
class LeafNode(HTMLNode):
  def __init__(self, value, tag=None, props=None):
    super().__init__(tag, value, None, props)
  
  def to_html(self):
    if self.value is None:
      raise ValueError("all leaf nodes must have a value")
    
    if self.tag is None:
      return self.value
    
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
  
class ParentNode(HTMLNode):
  def __init__(self, children, tag=None, props=None):
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.tag is None:
      raise ValueError("Invalid HTML: no tag")
    if self.children is None or len(self.children) == 0:
      raise ValueError("Invalid HTML: no children")
    children_html = ""
    for child in self.children:
      children_html += child.to_html()
    return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
  
  def __repr__(self):
    return f"ParentNode({self.tag}, children: {self.children}, {self.props})"