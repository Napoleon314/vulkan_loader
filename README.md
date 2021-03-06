Vulkan Loader
===
A simple lightweight function loader for Vulkan users having  preference of dynamic function loading preference

# Intruction
[Vulkan](https://www.khronos.org/vulkan/) a low-overhead, cross-platform 3D graphics and compute API first announced at GDC 2015 by the Khronos Group, which doesn't be like [Direct3D](https://en.wikipedia.org/wiki/Direct3D) made of [COM](https://msdn.microsoft.com/en-us/library/windows/desktop/ms680573(v=vs.85).aspx). This means it can not be used by dynamically loading only several COM Object creating functions. Of course, using [LunarG SDK](https://lunarg.com/vulkan-sdk/) could make this work easier, but the price is application will depend on the shared library of Vulkan loaded sucessfully. When I developing my [Venus3D](https://github.com/Napoleon314/Venus3D), I'd like to vertify Vulkan available on run-time so that I have to load all of Vulkan functions on run-time. To reduce workload, I used python to generate a head file with flexible macros which could do this work for me. This is possible because the Khronos Group released the [XML](https://en.wikipedia.org/wiki/XML) specifications of Vulkan and a generated header with prototype of Vulkan functions[(https://github.com/KhronosGroup/Vulkan-LoaderAndValidationLayers)](https://github.com/KhronosGroup/Vulkan-LoaderAndValidationLayers). As can be seen, there has already been a loader in the project of  the Khronos Group. However, this loader is rich and heavy with source code files which need to be compiled. Apparently, this is unnecessary, which is why I build this project to make a lightweight one.

# How to use
This ia a python file named vk_gen.py in the project which could be used by following ways:
```Bash
#with your preferred path to store the headers
python vk_gen.py ./vulkan
```
```Python
from vk_gen.py import vulkan_loader
if __name__ == "__main__":
	vk = vulkan_loader("vk.xml")
	#with your preferred path to store the headers
	vk.save("./vulkan")
```
There will be three headers generated in the specified location, which is called `vk_platform.h`, `vulkan.h` and `vulkan_loader.h`. Basically, only `vulkan_loader.h` is needed to be included in the source file which you are wondering to do initialization and termination about Vulkan. The following sample code is selected from the [VulkanRenderer of Venus3D](https://github.com/Napoleon314/Venus3D/blob/master/Source/Venus3D/Vulkan/VulkanRenderer.cpp):
```C++
#ifdef VE_ENABLE_VULKAN
#	if defined(BUILD_PLATFORM_WIN)
#		define VK_USE_PLATFORM_WIN32_KHR
#	elif defined(BUILD_PLATFORM_LINUX)
#		define VK_USE_PLATFORM_XLIB_KHR
#	endif
#	include "vulkan_loader.h"
#endif
#include "VulkanRenderer.h"

#ifdef VE_ENABLE_VULKAN

#ifdef THROW
#	undef THROW
#endif
#define THROW(...) VE_THROW("VulkanRenderer Error", __VA_ARGS__)

VK_LOADER_GLOBAL;//decl of global vars

#if defined(BUILD_PLATFORM_WIN)
#define LIB_VULKAN "vulkan-1.dll"
#elif defined(BUILD_PLATFORM_LINUX)
#define LIB_VULKAN "libvulkan.so"
#endif

void VulkanRenderer::Init()
{
	VK_LOADER_LOAD_ALL(LIB_VULKAN);//do init (param has to be the name of Vulkan lib)
	if (!VK_LOADER_HAS_LOADED())//vertify success
	{
		THROW("Failed to load " LIB_VULKAN ".");
	}
	VeCoreLogI("VulkanRenderer created successfully.");
}

void VulkanRenderer::Term()
{
	VK_LOADER_UNLOAD_ALL();//do term
}

#endif
```
# How it works
The principle of this python generator is really simple to understand. The vk.xml will be loaded and parsed to get the name of Vulkan commands(function called command in this XML file). Macros will be generated to `vulkan_loader.h`. The `VK_LOADER_GLOBAL` will declare necessary variables such as module handle and Vulkan function pointers with `_` prefix. `VK_LOADER_LOAD_ALL(name)` will load shared library (normally, namew will be `vulkan-1.dll` on Windows or `libvulkan.so` on Linux. If library loaded successfully, Vulkan function pointers will be filled one by one. The function set could be updated with the updating of specification file: `vk.xml`. `VK_LOADER_HAS_LOADED()` will check whether the library has been loaded successfully. Finally, `VK_LOADER_UNLOAD_ALL()` clears pointers to `NULL` and unloads the Vulkan module.

# Future works
Android will be supported when I porting my engine for android mobile system.

# Hope
It helps for Vulkan developers.

