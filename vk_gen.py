from xml.dom import minidom

class vulkan_loader:
	def __init__(self, xml):
		vk_doc = minidom.parse(xml)
		registry = vk_doc.documentElement
		comment = registry.getElementsByTagName("comment")
		for n in comment:
			print(n.childNodes[0].data)

	def save(self, path):
		print(path)

if __name__ == "__main__":
	vk = vulkan_loader("vk.xml")
	vk.save(".")
