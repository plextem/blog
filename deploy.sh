python3 -m mkdocs build --clean
echo "site/" > .gitignore
git add .
git commit -m 'blog'
git push origin master
python3 -m mkdocs gh-deploy
