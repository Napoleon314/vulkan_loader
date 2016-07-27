Vulkan Loader
===
A simple lightweight function loader for Vulkan users having  preference of dynamic function loading preference

# Intruction
[Vulkan](https://www.khronos.org/vulkan/) a low-overhead, cross-platform 3D graphics and compute API first announced at GDC 2015 by the Khronos Group, which doesn't be like [Direct3D](https://en.wikipedia.org/wiki/Direct3D) made of [COM](https://msdn.microsoft.com/en-us/library/windows/desktop/ms680573(v=vs.85).aspx). This means it can not be used by dynamically loading only several COM Object creating functions. Of course, using [LunarG SDK](https://lunarg.com/vulkan-sdk/) could make this work easier, but the price is application will depend on the shared library of Vulkan loaded sucessfully. When I developing my [Venus3D](https://lunarg.com/vulkan-sdk/), I'd like to vertify Vulkan available on run-time so that I have to load all of Vulkan functions on run-time. To reduce workload, I used python to generate a head file with flexible macros which could do this work for me. This is possible because the Khronos Group released the [XML](https://en.wikipedia.org/wiki/XML) specifications of Vulkan and a generated header with prototype of Vulkan functions[(https://github.com/KhronosGroup/Vulkan-LoaderAndValidationLayers)](https://github.com/KhronosGroup/Vulkan-LoaderAndValidationLayers). As can be seen, there has already been a loader in the project of  the Khronos Group. However, this loader is rich and heavy with source code files which need to be compiled. Apparently, this is unnecessary, which is why I build this project to make a lightweight one.

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


