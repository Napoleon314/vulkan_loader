import os, sys, shutil
from xml.dom import minidom

class vulkan_extension:
	def __init__(self, ext):
		if ext.hasAttribute("protect"):
			self.protect = ext.getAttribute("protect")
		else:
			self.protect = ""
		self.command_vec = []
		for cmd in ext.getElementsByTagName("require")[0].getElementsByTagName("command"):
			self.command_vec.append(cmd.getAttribute("name"))

class vulkan_loader:
	def __init__(self, xml):
		try:
			self.xml_root = minidom.parse(xml).documentElement
			self.extension_vec = []
			self.extension_dict = {}
			self.ext_command_dict = {}
			for ext in self.xml_root.getElementsByTagName("extensions")[0].getElementsByTagName("extension"):
				name = ext.getAttribute("name")
				self.extension_vec.append(name)
				obj = vulkan_extension(ext)
				self.extension_dict[name] = obj
				for cmd in obj.command_vec:
					self.ext_command_dict[cmd] = name
			self.command_dict = []
			for command in self.xml_root.getElementsByTagName("commands")[0].getElementsByTagName("command"):
				cmd = command.getElementsByTagName("proto")[0].getElementsByTagName("name")[0].firstChild.data
				if cmd not in self.ext_command_dict:
					self.command_dict.append(cmd)
		except:
			print("Parse xml spec error.")
			exit()

	def add_line(self, line):
		self.vulkan_loader_content += line + "\n"

	def add_comments(self):
		print("\tadd comments for vulkan_loader.h")
		self.add_line("////////////////////////////////////////////////////////////////////////////")
		for line in self.xml_root.getElementsByTagName("comment")[0].childNodes[0].data.split('\n'):
			self.add_line("//  " + line)
		self.add_line("//  ------------------------------------------------------------------------")
		self.add_line("//")
		self.add_line("//  Vulkan loader is generated for dynamically loading function of vulkan on")
		self.add_line("//  Windows and Linux.")
		self.add_line("//  This generator is written by Albert D Yang.")
		self.add_line("//")
		self.add_line("////////////////////////////////////////////////////////////////////////////")
		self.add_line("")

	def add_commands(self):
		print("\tadd commands for vulkan_loader.h")
		global_func = "#define VK_LOADER_GLOBAL_FUNC"
		protected_func = []
		for cmd in self.command_dict:
			self.add_line("extern PFN_" + cmd + " _" + cmd + ";")
			self.add_line("#define " + cmd + " _" + cmd)
			self.add_line("")
			global_func += " \\\n\tPFN_" + cmd + " _" + cmd + " = NULL;"
		for ext in self.extension_vec:
			obj = self.extension_dict[ext]
			if len(obj.command_vec):
				self.add_line("/* " + ext + " */")
				if obj.protect != "":
					self.add_line("#ifdef " + obj.protect)
					self.add_line("")
				for cmd in obj.command_vec:
					self.add_line("extern PFN_" + cmd + " _" + cmd + ";")
					self.add_line("#define " + cmd + " _" + cmd)
					self.add_line("")
				if obj.protect != "":
					self.add_line("#endif ")
					self.add_line("")
					_func = "#ifdef " + obj.protect + "\n#define " + obj.protect + "_GLOBAL_FUNC"
					for cmd in obj.command_vec:
						_func += " \\\n\tPFN_" + cmd + " _" + cmd + " = NULL;"
					_func += "\n#else\n#define " + obj.protect + "_GLOBAL_FUNC\n#endif"
					protected_func.append(_func)
				else:
					for cmd in obj.command_vec:
						global_func += " \\\n\tPFN_" + cmd + " _" + cmd + " = NULL;"

		self.add_line(global_func)
		for func in protected_func:
			self.add_line("")
			self.add_line(func)
		self.add_line("")
		self.add_line("#if defined(VK_USE_PLATFORM_WIN32_KHR)")
		self.add_line("#define VK_LOADER_STATIC_MODULE_HANDLE static HMODULE _vkModule = NULL;")
		self.add_line("#elif defined(VK_USE_PLATFORM_XLIB_KHR)")
		self.add_line("#define VK_LOADER_STATIC_MODULE_HANDLE static void* _vkModule = NULL;")
		self.add_line("#else")
		self.add_line("#define VK_LOADER_STATIC_MODULE_HANDLE static int _vkModule = 0;")
		self.add_line("#endif")
		self.add_line("")
		global_macro = "#define VK_LOADER_GLOBAL \\\n\tVK_LOADER_STATIC_MODULE_HANDLE; \\\n\tVK_LOADER_GLOBAL_FUNC;"
		for ext in self.extension_vec:
			obj = self.extension_dict[ext]
			if obj.protect != "":
				global_macro += " \\\n\t" + obj.protect + "_GLOBAL_FUNC;"
		self.add_line(global_macro)
		self.add_line("")

		self.add_line("#if defined(VK_USE_PLATFORM_WIN32_KHR)")
		self.add_line("#define VK_LOADER_LOAD_MODULE(n) if(!_vkModule) _vkModule = LoadLibraryA(n)")
		self.add_line("#define VK_LOADER_UNLOAD_MODULE() if(_vkModule) {FreeLibrary(_vkModule);_vkModule = NULL;}")
		self.add_line("#define VK_LOADER_GET_PROC(proc) GetProcAddress(_vkModule, proc)")
		self.add_line("#elif defined(VK_USE_PLATFORM_XLIB_KHR)")
		self.add_line("#define VK_LOADER_LOAD_MODULE(n) if(!_vkModule) _vkModule = dlopen(n, RTLD_LAZY | RTLD_GLOBAL)")
		self.add_line("#define VK_LOADER_UNLOAD_MODULE() if(_vkModule) {dlclose(_vkModule);_vkModule = NULL;}")
		self.add_line("#define VK_LOADER_GET_PROC(proc) dlsym(_vkModule, proc)")
		self.add_line("#else")
		self.add_line("#define VK_LOADER_LOAD_MODULE(n)")
		self.add_line("#define VK_LOADER_UNLOAD_MODULE()")
		self.add_line("#define VK_LOADER_GET_PROC(proc)")
		self.add_line("#endif")
		self.add_line("")
		self.add_line("#define VK_LOADER_HAS_LOADED() (_vkModule != 0)")
		self.add_line("")
		
		load_macro = "#define VK_LOADER_LOAD_ALL(n) \\\n\tVK_LOADER_LOAD_MODULE(n); \\\n\tif(_vkModule) {"
		unload_macro = "#define VK_LOADER_UNLOAD_ALL() \\\n\tVK_LOADER_UNLOAD_MODULE();"
		for cmd in self.command_dict:
			self.add_line("#define VK_LOADER_LOAD_" + cmd + " _" + cmd + " = (PFN_" + cmd + ")VK_LOADER_GET_PROC(\"" + cmd + "\")")
			load_macro += " \\\n\t\tVK_LOADER_LOAD_" + cmd + ";"
			unload_macro += " \\\n\t_" + cmd + " = NULL;"

		for ext in self.extension_vec:
			obj = self.extension_dict[ext]
			if len(obj.command_vec):
				if obj.protect != "":
					self.add_line("#ifdef " + obj.protect)
					for cmd in obj.command_vec:
						self.add_line("#define VK_LOADER_LOAD_" + cmd + " _" + cmd + " = (PFN_" + cmd + ")VK_LOADER_GET_PROC(\"" + cmd + "\")")
						self.add_line("#define VK_LOADER_UNLOAD_" + cmd + " _" + cmd + " = NULL")
					self.add_line("#else")
					for cmd in obj.command_vec:
						self.add_line("#define VK_LOADER_LOAD_" + cmd)
						self.add_line("#define VK_LOADER_UNLOAD_" + cmd)
						load_macro += " \\\n\t\tVK_LOADER_LOAD_" + cmd + ";"
						unload_macro += " \\\n\tVK_LOADER_UNLOAD_" + cmd + ";"
					self.add_line("#endif")
				else:
					for cmd in obj.command_vec:
						self.add_line("#define VK_LOADER_LOAD_" + cmd + " _" + cmd + " = (PFN_" + cmd + ")VK_LOADER_GET_PROC(\"" + cmd + "\")")
						load_macro += " \\\n\t\tVK_LOADER_LOAD_" + cmd + ";"
						unload_macro += " \\\n\t_" + cmd + " = NULL;"


		load_macro += " \\\n\t}"

		self.add_line("")
		self.add_line(load_macro)
		self.add_line("")
		self.add_line(unload_macro)
		self.add_line("")

	def create_vulkan_loader(self):
		print("generating vulkan_loader.h...")
		self.vulkan_loader_content = ""
		self.add_comments()
		self.add_line("#ifndef VULKAN_LOADER_H_")
		self.add_line("#define VULKAN_LOADER_H_ 1")
		self.add_line("")
		self.add_line("#include \"vulkan.h\"")
		self.add_line("")
		self.add_commands()
		self.add_line("#endif")

	def save_vulkan_loader(self, path):
		print("saving vulkan_loader.h...")
		vulkan_loader_h = open(path + "/vulkan_loader.h", "w")
		vulkan_loader_h.write(self.vulkan_loader_content)
		vulkan_loader_h.close()

	def save(self, path):
		if path == ".":
			target_path = "vulkan"
		else:
			target_path = path
		if not os.path.isdir(target_path):
			print("Making directory: " + target_path + " ...")
			os.makedirs(target_path)
		print("copying vk_platform.h to " + target_path)
		shutil.copyfile("vk_platform.h", target_path + "/vk_platform.h")
		print("copying vulkan.h to " + target_path)
		shutil.copyfile("vulkan.h", target_path + "/vulkan.h")
		self.create_vulkan_loader()
		self.save_vulkan_loader(target_path)

if __name__ == "__main__":
	vk = vulkan_loader("vk.xml")
	if len(sys.argv) > 1:
		vk.save(sys.argv[1])
	else:
		vk.save(".")
