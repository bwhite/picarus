set -e
# Build new docs
rm -rf html
make html

# Copy relevant files to doc_temp
pushd ..
rm -rf doc_temp
cp -R doc doc_temp

# Ignore the current git changes so we can switch to gh-pages
git stash
git checkout gh-pages

# Ensure that .nojekyll is set for github to ignore _'d dirs
touch .nojekyll
git add .nojekyll

# Remove previous docs and update git
rm -fr _*
mv ./doc_temp/html/* .
git add -u
git add ./_*
git commit -m "Bump"
git push

# Switch back to master, revert changes, and cleanup
git checkout master
git stash apply
rm -rf doc_temp
popd