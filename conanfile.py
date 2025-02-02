from conans import ConanFile, tools, MSBuild
import os


class PthreadWin32Conan(ConanFile):
    name = "pthread-win32"
    version = "2.9.1"
    description = "Keep it short"
    url = "https://github.com/ulricheck/conan-pthread-win32"
    homepage = "http://www.sourceware.org/pthreads-win32/"
    license = "GNU LGPL"
    exports = ["LICENSE.md"]

    # Options may need to change depending on the packaged library.
    settings = {"os": "Windows", "arch": None, "compiler": "Visual Studio", "build_type": None}
    options = {"shared": [True, False]}
    default_options = {'shared': 'False'}
    _source_subfolder = "source_subfolder"

    def source(self):
        tools.get("https://github.com/GerHobbelt/pthread-win32/archive/master.zip")
        os.rename('pthread-win32-master', self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            solution_name = {15: 'pthread.2015.sln',
                             14: 'pthread.2015.sln',
                             12: 'pthread.2013.sln'}.get(int(str(self.settings.compiler.version)))
            targets = ['pthread_dll'] if self.options.shared else ['pthread_lib']
            msbuild = MSBuild(self)
            msbuild.build(solution_name, targets=targets, platforms={"x86": "Win32"})

    def package(self):
        self.copy(pattern="LICENSE", dst="COPYING", src=self._source_subfolder)
        self.copy(pattern="pthread.h", dst="include", src=self._source_subfolder)
        self.copy(pattern="sched.h", dst="include", src=self._source_subfolder)
        self.copy(pattern="semaphore.h", dst="include", src=self._source_subfolder)
        self.copy(pattern="*.dll", dst="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['pthread_dll' if self.options.shared else 'pthread_lib']
        if not self.options.shared:
            self.cpp_info.defines.append('PTW32_STATIC_LIB=1')
