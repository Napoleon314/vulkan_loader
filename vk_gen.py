import os, sys
from xml.dom import minidom

class vulkan_loader:
	def __init__(self, xml):
		vk_doc = minidom.parse(xml)
		registry = vk_doc.documentElement
		comment = registry.getElementsByTagName("comment")
		self.vulkan_h_content = ""
		for n in comment:
			self.vulkan_h_content += n.childNodes[0].data

	def save(self, path):
		target_path = path + "/vulkan"
		if not os.path.isdir(target_path):
			print("Making directory: " + target_path + " ...")
			os.makedirs(target_path)
		vulkan_h = open(target_path+'/vulkan.h', 'w')
		vulkan_h.write(self.vulkan_h_content)
		vulkan_h.close()
		#print(path)

if __name__ == "__main__":
	vk = vulkan_loader("vk.xml")
	vk.save(".")
