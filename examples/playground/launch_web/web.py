from pynpm import NPMPackage

pkg = NPMPackage('../../../web/eyegway-svelte/package.json')
# pkg.install()
# pkg.build()
pkg.run_script('build')
pkg.run_script('preview')
