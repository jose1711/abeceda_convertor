# builds a deb package for debian and derivatives
BUILDDIR = ./abeceda_convertor.build
font_url = http://www.cpppap.svsbb.sk/download/font/Abeceda.zip

make_deb:
	# get the latest font
	wget -q --output-document=- "${font_url}" | bsdtar -xvOf - > Abeceda_v4.ttf
	mkdir -p "${BUILDDIR}/usr/share/applications"
	mkdir -p "${BUILDDIR}/usr/share/icons"
	install -m644 abeceda_convertor.desktop "${BUILDDIR}/usr/share/applications"
	install -m644 abeceda_convertor.svg "${BUILDDIR}/usr/share/icons/hicolor/scalable/apps"
	install -Dm755 abeceda.py "${BUILDDIR}/usr/bin/abeceda.py"
	install -Dm644 Abeceda_v4.ttf "${BUILDDIR}/usr/share/fonts/TTF/Abeceda_v4.ttf"
	cp -r DEBIAN "${BUILDDIR}"
	dpkg-deb --build "${BUILDDIR}" abeceda.deb

clean:
	rm -r "${BUILDDIR}"
	rm abeceda.deb Abeceda_v4.ttf
