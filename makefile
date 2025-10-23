# name
name = fhirproof

docdir = ~/numlims.github.io/fhirproof/
docmake = ~/numlims.github.io

# get the version from github tag
# sort by version; get the last line; delete the v from the version tag cause python build seems to strip it as well
version = $(shell git tag | sort -V | tail -1 | tr -d v)

.PHONY: test

all:
	cd fhirproof; make
	ct test/test_db.ct
	ct test/test_nodb.ct

build:
	make
	python3 -m build --no-isolation

test:
	make install
	pytest -s
install:
	make build
	pip install "./dist/${name}-${version}-py3-none-any.whl" --no-deps --force-reinstall

doc:
	make
	pdoc "./${name}" -o html

doc-publish:
	make doc
	cp -r html/* ${docdir}
	cd ${docmake} && make publish

publish:
	make build
	make doc-publish
	git push --tags
	gh release create "v${version}" "./dist/${name}-${version}-py3-none-any.whl"

publish-update: # if an asset was already uploaded, delete it before uploading again
	make build
	make doc-publish
	# does the tag updating also update the source code at the resource?
	# move the version tag to the most recent commit
	git tag -f "v${version}"
	# delete tag on remote
	git push origin ":refs/tags/v${version}" 
	# re-push the tag to the remote
	git push --tags
	gh release delete-asset "v${version}" "${name}-${version}-py3-none-any.whl" -y
	gh release upload "v${version}" "./dist/${name}-${version}-py3-none-any.whl"
	# apparently the tag change rolled the release back to draft, set it to publish again
	gh release edit "v${version}" --draft=false

