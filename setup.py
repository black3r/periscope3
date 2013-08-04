from setuptools import setup
import periscopeversion

PACKAGE = 'periscope'

setup(name = PACKAGE, version = periscopeversion.VERSION,
      license = "GPL version 2",
      description = "Python 3 module to download subtitles for a given video file",
      author = "Roman Hudec",
      author_email = "black3r@klikni.cz",
      url = "https://github.com/black3r/periscope3/",
      packages= [ "periscope", "periscope/plugins" ],
      py_modules=["periscope"],
      scripts = [ "scripts/periscope3" ],
      install_requires = ["beautifulsoup4 >= 4.2.1"]
      )
