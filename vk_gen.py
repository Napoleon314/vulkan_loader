import os, sys
from xml.dom import minidom

class vulkan_loader:
	def __init__(self, xml):
		try:
			self.xml_root = minidom.parse(xml).documentElement
		except:
			print("Parse xml spec error.")
			exit()

	def add_line_vulkan_h(self, line):
		self.vulkan_h_content += line + "\n"

	def add_comments_vulkan_h(self):
		print("\tadd comments for vulkan.h")
		self.add_line_vulkan_h("////////////////////////////////////////////////////////////////////////////")
		for line in self.xml_root.getElementsByTagName("comment")[0].childNodes[0].data.split('\n'):
			self.add_line_vulkan_h("//  " + line)
		self.add_line_vulkan_h("////////////////////////////////////////////////////////////////////////////")
		self.add_line_vulkan_h("")

	def add_type_vulkan_h(self, type_element):
		print(type_element.nodeType)

	def add_types_vulkan_h(self):
		print("\tadd types for vulkan.h")
		types = self.xml_root.getElementsByTagName("types")[0].childNodes
		
		print(types[0].data)
		#for i in range(types.length):
		#	self.add_type_vulkan_h(types[i])

	def create_vulkan_h(self):
		print("generating vulkan.h...")
		self.vulkan_h_content = ""
		self.add_line_vulkan_h("#ifndef VULKAN_H_")
		self.add_line_vulkan_h("#define VULKAN_H_ 1")
		self.add_line_vulkan_h("")
		self.add_line_vulkan_h("#ifdef __cplusplus")
		self.add_line_vulkan_h("extern \"C\" {")
		self.add_line_vulkan_h("#endif")
		self.add_line_vulkan_h("")
		self.add_comments_vulkan_h()
		self.add_types_vulkan_h()
		self.add_line_vulkan_h("")
		self.add_line_vulkan_h("#ifdef __cplusplus")
		self.add_line_vulkan_h("}")
		self.add_line_vulkan_h("#endif")
		self.add_line_vulkan_h("")
		self.add_line_vulkan_h("#endif")
		self.add_line_vulkan_h("")
		print("vulkan.h has been generated.")

	def save(self, path):
		target_path = path + "/vulkan"
		if not os.path.isdir(target_path):
			print("Making directory: " + target_path + " ...")
			os.makedirs(target_path)
		self.create_vulkan_h()
		vulkan_h = open(target_path+'/vulkan.h', 'w')
		vulkan_h.write(self.vulkan_h_content)
		vulkan_h.close()
		print("vulkan.h has been saved to " + target_path)

if __name__ == "__main__":
	vk = vulkan_loader("vk.xml")
	vk.save(".")
