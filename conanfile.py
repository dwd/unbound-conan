from conan import ConanFile
from conan.tools.gnu import Autotools, AutotoolsDeps, AutotoolsToolchain
from conan.tools.files import copy, get

class MyLibraryConan(ConanFile):
    name = "unbound"
    license = "BSD-3-Clause"
    url = "https://github.com/NLNetLabs/unbound"
    description = "Library only build of unbound, a DNS library"
    topics = ("dns", "dnssec", "async")
    settings = "os", "compiler", "build_type", "arch"
    exports_sources = "."
    tool_requires = "flex/2.6.4", "bison/3.8.2"

    def requirements(self):
        self.requires("openssl/[>=1.1 <4]")
        self.requires("zlib/[>=1.2.11 <2]")
        self.requires("libevent/[>=2.1.0 <3]")

    def source(self):
        upstream_version = self.version.split('_')[0]
        get(self, url=f"https://github.com/NLnetLabs/unbound/archive/refs/tags/release-{upstream_version}.tar.gz", strip_root=True)

    def generate(self):
        tc = AutotoolsToolchain(self)
        tc.configure_args.append("--with-libunbound-only")
        tc.configure_args.append(f"--with-libevent={self.dependencies['libevent'].package_folder}")
        tc.configure_args.append(f"--with-ssl={self.dependencies['openssl'].package_folder}")
        tc.configure_args.append("--with-pthreads")
        tc.configure_args.append("--disable-shared")
        tc.configure_args.append("--with-pic")
        tc.generate()
        deps = AutotoolsDeps(self)
        deps.generate()

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        at = Autotools(self)
        at.install()

    def package_info(self):
        self.cpp_info.libs = ["unbound"]

