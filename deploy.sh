mkdocs build
git add .
git commit -m 'blog'
git push origin master
mkdocs gh-deploy
