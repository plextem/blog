python -m mkdocs build --clean
echo "site/" > .gitignore
git add .
git commit -m 'blog'
git push origin master
python -m mkdocs gh-deploy
