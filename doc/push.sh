set -e
# Build new docs
rm -rf html
make html
rm -rf _build

# Copy relevant files to doc_temp
pushd ..
rm -rf doc_temp
cp -R doc/html doc_temp

# Ignore the current git changes so we can switch to gh-pages
git stash

# Remove previous files and branch
#rm -fr _* *.html *.js *.inv
git branch -d gh-pages
git checkout --orphan gh-pages

# Ensure that .nojekyll is set for github to ignore _'d dirs
touch .nojekyll
git add .nojekyll

# Update git
mv ./doc_temp/* .
git add -u
git add *.html
git add *.js
git add *.inv
git add ./_*
git commit -m "Bump"
git push -f

# Switch back to master, revert changes, and cleanup
git checkout master
git stash apply
rm -rf doc_temp
popd